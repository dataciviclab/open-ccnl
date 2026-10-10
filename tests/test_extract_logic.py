"""Logica pura degli extract (niente rete)."""

from __future__ import annotations

import importlib.util
from pathlib import Path

import pytest

REPO = Path(__file__).resolve().parents[1]


def _load(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, path)
    assert spec and spec.loader
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


@pytest.mark.pure_unit
def test_applicazione_header_normalization_and_year_map() -> None:
    mod = _load(
        "extract_applicazione",
        REPO / "datasets" / "ccnl-applicazione" / "extract.py",
    )
    headers = [
        "CCNL id",
        "status",
        "n° datori di lavoro 2018",
        "n° dipendenti 2018",
        "n° datori di lavoro  2021",
        "n° dipendenti F 2023",
        "n° dipendenti M 2023",
        "n° dipendenti 2023",
    ]
    norm = [mod._norm_header(h) for h in headers]
    assert norm[2] == "n° datori di lavoro 2018"
    assert norm[4] == "n° datori di lavoro 2021"

    year_cols = mod._resolve_year_columns(norm)
    assert year_cols[2018]["datori"] == 2
    assert year_cols[2018]["dipendenti"] == 3
    assert year_cols[2021]["datori"] == 4
    assert year_cols[2023]["dipendenti_f"] == 5
    assert year_cols[2023]["dipendenti_m"] == 6
    assert year_cols[2023]["dipendenti"] == 7


@pytest.mark.pure_unit
def test_to_int_italian_and_plain() -> None:
    mod = _load(
        "extract_applicazione",
        REPO / "datasets" / "ccnl-applicazione" / "extract.py",
    )
    assert mod._to_int(12) == 12
    assert mod._to_int(12.0) == 12
    assert mod._to_int("1.234") == 1234
    assert mod._to_int("1234") == 1234
    assert mod._to_int("") is None
    assert mod._to_int(None) is None
    assert mod._to_int(True) is None


@pytest.mark.pure_unit
def test_metadata_join_list() -> None:
    mod = _load(
        "extract_metadata",
        REPO / "datasets" / "ccnl-metadata" / "extract.py",
    )
    assert mod._join(["A", " B ", None]) == "A;B"
    assert mod._join(True) == "true"
    assert mod._join(None) == ""
    assert mod._join(" x ") == "x"


@pytest.mark.pure_unit
def test_argomenti_trim_date_and_row_mapping() -> None:
    mod = _load(
        "extract_argomenti",
        REPO / "datasets" / "ccnl-argomenti" / "extract.py",
    )
    assert mod._trim_date("2021-12-06T00:00:00") == "2021-12-06"
    assert mod._trim_date(None) == ""
    assert mod._trim_date("") == ""

    tax = {
        "codice": "CR5",
        "nome": "Trattamento di fine rapporto",
        "codice_macro": "CR",
        "nome_macro": "CESSAZIONE DEL RAPPORTO",
    }
    item = {
        "idAccordo": 140725,
        "codiceCcnl": " e015 ",
        "tipologiaAccordo": "Accordo di rinnovo",
        "dataStipula": "2021-12-06",
        "dataDecorrenza": None,
        "dataScadenzaContrattuale": "2022-12-31",
        "titoloCcnl": "CCNL alimentari",
        "settoriAtecoAccordo": ["E", "E01"],
        "statoAA": "pubblicata",
        "ultimoAccordoVigente": True,
    }
    row = mod.row_from_api(item, tax)
    assert row["id_accordo"] == 140725
    assert row["codice_ccnl"] == "E015"
    assert row["codice_argomento"] == "CR5"
    assert row["codice_macro"] == "CR"
    assert row["data_decorrenza"] == ""
    assert row["settori_ateco"] == "E;E01"
    assert row["ultimo_accordo_vigente"] == "true"
