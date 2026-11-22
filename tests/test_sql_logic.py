"""Semantica dei mart: missing, genere, anno di riferimento, rinnovi.

I test eseguono i file SQL reali su un piccolo clean_input in DuckDB.
"""

from __future__ import annotations

import datetime as dt
from pathlib import Path

import duckdb
import pytest

REPO = Path(__file__).resolve().parents[1]

APPLICAZIONE_COLS = """
    codice_ccnl VARCHAR, anno INTEGER, titolo VARCHAR, status VARCHAR,
    tipo_ccnl VARCHAR, sottosezione VARCHAR, is_conto_annuale_ppaa BOOLEAN,
    n_datori BIGINT, n_dipendenti BIGINT, n_dipendenti_f BIGINT,
    n_dipendenti_m BIGINT, filtri_conto_annuale_ppaa VARCHAR
"""

METADATA_COLS = """
    archivio VARCHAR, codice_ccnl VARCHAR, titolo_ccnl VARCHAR,
    tipologia_accordo VARCHAR, data_stipula DATE, data_decorrenza DATE,
    data_scadenza_contrattuale DATE, data_pubblicazione DATE,
    ultimo_accordo_vigente BOOLEAN, stato_aa VARCHAR
"""


def _run(sql_rel: str, columns: str, rows: list[tuple]) -> list[dict]:
    con = duckdb.connect()
    con.execute(f"CREATE TABLE clean_input ({columns})")
    placeholders = ", ".join("?" for _ in rows[0])
    con.executemany(f"INSERT INTO clean_input VALUES ({placeholders})", rows)
    cur = con.execute((REPO / sql_rel).read_text(encoding="utf-8"))
    names = [d[0] for d in cur.description]
    result = [dict(zip(names, row, strict=True)) for row in cur.fetchall()]
    con.close()
    return result


def _apply_row(
    code: str,
    year: int,
    *,
    pa: bool = False,
    n: int = 0,
    f: int = 0,
    m: int = 0,
    datori: int = 0,
    title: str | None = None,
) -> tuple:
    return (
        code,
        year,
        title or code,
        "vigente",
        "pubblico" if pa else "privato",
        "Settore pubblico" if pa else "CCNL settore vigenti o ultrattivi",
        pa,
        datori,
        n,
        f,
        m,
        "comparto: test" if pa else None,
    )


@pytest.mark.pure_unit
def test_top_gender_is_null_when_fm_missing() -> None:
    rows = [
        _apply_row("PRIV", 2025, n=1000, f=400, m=600, datori=10),
        _apply_row("PA", 2025, pa=True, n=1000, f=0, m=0),
    ]
    got = {r["codice_ccnl"]: r for r in _run("datasets/ccnl-applicazione/sql/mart_ccnl_top.sql", APPLICAZIONE_COLS, rows)}

    assert got["PRIV"]["quota_dipendenti_f"] == pytest.approx(0.4)
    assert got["PRIV"]["genere_disponibile"] is True
    assert got["PA"]["quota_dipendenti_f"] is None
    assert got["PA"]["genere_disponibile"] is False
    assert got["PA"]["is_conto_annuale_ppaa"] is True
    assert got["PA"]["anno_riferimento"] == 2025


@pytest.mark.pure_unit
def test_classifica_uses_latest_year_with_pa() -> None:
    rows = [
        _apply_row("A", 2024, n=100),
        _apply_row("B", 2024, pa=True, n=200),
        _apply_row("A", 2025, n=150),
        # 2025 senza PA: B resta a 0 e non deve entrare nella classifica
        _apply_row("B", 2025, pa=True, n=0),
    ]
    got = _run("datasets/ccnl-applicazione/sql/mart_ccnl_classifica.sql", APPLICAZIONE_COLS, rows)

    assert {r["anno_riferimento"] for r in got} == {2024}
    by_code = {r["codice_ccnl"]: r for r in got}
    assert by_code["A"]["n_dipendenti"] == 100
    assert by_code["B"]["n_dipendenti"] == 200
    assert by_code["B"]["rank_nazionale"] == 1
    assert by_code["A"]["rank_nazionale"] == 2


@pytest.mark.pure_unit
def test_totali_anno_flags_pa_and_gender_denominator() -> None:
    rows = [
        _apply_row("A", 2024, n=100, f=40, m=60),
        _apply_row("B", 2024, pa=True, n=200, f=0, m=0),
        _apply_row("A", 2025, n=150, f=60, m=90),
        _apply_row("B", 2025, pa=True, n=0, f=0, m=0),
    ]
    got = {r["anno"]: r for r in _run("datasets/ccnl-applicazione/sql/mart_ccnl_totali_anno.sql", APPLICAZIONE_COLS, rows)}

    assert got[2024]["pa_inclusa"] is True
    assert got[2025]["pa_inclusa"] is False
    assert got[2024]["n_dipendenti"] == 300
    assert got[2024]["quota_donne_fm_pct"] == pytest.approx(40.0)
    assert got[2024]["quota_donne_totale_pct"] == pytest.approx(13.3)
    assert got[2025]["quota_donne_fm_pct"] == pytest.approx(40.0)


@pytest.mark.pure_unit
def test_serie_gender_and_pa_flag() -> None:
    rows = [
        _apply_row("A", 2024, n=100, f=40, m=60),
        _apply_row("B", 2024, pa=True, n=200, f=0, m=0),
        _apply_row("A", 2025, n=150, f=60, m=90),
        _apply_row("B", 2025, pa=True, n=0, f=0, m=0),
    ]
    got = _run("datasets/ccnl-applicazione/sql/mart_ccnl_serie.sql", APPLICAZIONE_COLS, rows)
    by_key = {(r["codice_ccnl"], r["anno"]): r for r in got}

    assert by_key[("B", 2024)]["genere_disponibile"] is False
    assert by_key[("B", 2024)]["quota_dipendenti_f"] is None
    assert by_key[("B", 2024)]["pa_inclusa"] is True
    assert by_key[("A", 2025)]["quota_dipendenti_f"] == pytest.approx(0.4)
    assert by_key[("A", 2024)]["pa_inclusa"] is True


@pytest.mark.pure_unit
def test_rinnovi_use_latest_agreement_not_only_definitive() -> None:
    rows = [
        (
            "ARCHIVIO_CORRENTE",
            "B011",
            "Chimica",
            "Testo definitivo",
            dt.date(2022, 6, 13),
            dt.date(2022, 6, 13),
            dt.date(2025, 6, 30),
            dt.date(2022, 7, 1),
            True,
            "Pubblicato",
        ),
        (
            "ARCHIVIO_CORRENTE",
            "B011",
            "Chimica",
            "Accordo di rinnovo",
            dt.date(2025, 4, 15),
            dt.date(2025, 4, 15),
            dt.date(2028, 6, 30),
            dt.date(2025, 5, 1),
            True,
            "Pubblicato",
        ),
        (
            "ARCHIVIO_CORRENTE",
            "OLD",
            "Vecchio",
            "Testo definitivo",
            dt.date(2020, 1, 1),
            dt.date(2020, 1, 1),
            dt.date(2020, 12, 31),
            dt.date(2020, 2, 1),
            True,
            "Pubblicato",
        ),
    ]
    got = {r["codice_ccnl"]: r for r in _run("datasets/ccnl-metadata/sql/mart_ccnl_rinnovi.sql", METADATA_COLS, rows)}

    assert got["B011"]["tipologia_ultimo_accordo"] == "Accordo di rinnovo"
    assert got["B011"]["data_scadenza"] == dt.date(2028, 6, 30)
    assert got["B011"]["scaduto"] is False
    assert got["OLD"]["scaduto"] is True
    assert got["OLD"]["giorni_scaduto"] > 0
