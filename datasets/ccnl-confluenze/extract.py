#!/usr/bin/env python3
"""Scarica gli Excel CNEL di riepilogativo e principali storici ed estrae
la mappa delle confluenze dei codici CCNL.

Uso: python3 extract.py raw.csv
"""

from __future__ import annotations

import csv
import io
import sys
import urllib.request
from pathlib import Path

RIEPILOGATIVO_URL = (
    "https://www.cnel.it/media/docs/default-source/"
    "archivio-contratti---cartelle-excel/"
    "documento-riepilogativo-testi-depositati.xlsx"
)
STORICI_URL = (
    "https://www.cnel.it/media/docs/default-source/"
    "archivio-contratti---cartelle-excel/"
    "principali-ccnl-storici.xlsx"
)

COLUMNS = [
    "fonte",
    "codice_confluito",
    "confluenze_intermedie",
    "codice_vigente",
    "titolo_confluito",
    "titolo_vigente",
    "sezione_ateco",
    "sezione_ateco_desc",
    "inizio_storia",
    "fine_storia",
]


def _norm(value: object) -> str:
    if value is None:
        return ""
    return " ".join(str(value).split())


def _date(value: object) -> str:
    if value is None or value == "":
        return ""
    if hasattr(value, "isoformat"):
        try:
            return value.isoformat()[:10]  # type: ignore[no-any-return]
        except Exception:
            return str(value)
    text = str(value).strip()
    return text[:10] if len(text) >= 10 else text


def download(url: str) -> bytes:
    print(f"  download {url}", flush=True)
    req = urllib.request.Request(url, headers={"User-Agent": "dataciviclab-open-ccnl/0.1"})
    with urllib.request.urlopen(req, timeout=180) as resp:
        data = resp.read()
    print(f"  {len(data)} bytes")
    return data


def _sheet_by_keyword(wb, *keywords: str):
    for name in wb.sheetnames:
        low = name.lower()
        if all(k in low for k in keywords):
            return wb[name]
    return None


def _header_index(headers: list[str]) -> dict[str, int]:
    return {h: i for i, h in enumerate(headers) if h}


def extract_confluenze_riepilogativo(xlsx: bytes) -> list[dict]:
    from openpyxl import load_workbook

    wb = load_workbook(io.BytesIO(xlsx), read_only=True, data_only=True)
    ws = _sheet_by_keyword(wb, "confluenz")
    if ws is None:
        # fallback: seconda scheda dati
        data_sheets = [s for s in wb.sheetnames if "guida" not in s.lower()]
        if not data_sheets:
            raise RuntimeError(f"Nessun foglio dati. Sheets: {wb.sheetnames}")
        ws = wb[data_sheets[-1]]

    rows_iter = ws.iter_rows(values_only=True)
    header = [_norm(h).lower() for h in (next(rows_iter) or ())]
    idx = _header_index(header)

    def col(*frags: str) -> int | None:
        for i, h in enumerate(header):
            if all(f in h for f in frags):
                return i
        return None

    i_from = col("confluito", "id") or col("ccnl id confluito")
    i_via = col("intermedie")
    i_to = col("vigente") or col("ccnl id vigente")
    if i_from is None:
        raise RuntimeError(f"Colonne confluenze non riconosciute: {header}")

    out: list[dict] = []
    for row in rows_iter:
        if row is None:
            continue
        code_from = _norm(row[i_from]) if i_from < len(row) else ""
        if not code_from:
            continue
        out.append(
            {
                "fonte": "documento_riepilogativo",
                "codice_confluito": code_from,
                "confluenze_intermedie": _norm(row[i_via]) if i_via is not None and i_via < len(row) else "",
                "codice_vigente": _norm(row[i_to]) if i_to is not None and i_to < len(row) else "",
                "titolo_confluito": "",
                "titolo_vigente": "",
                "sezione_ateco": "",
                "sezione_ateco_desc": "",
                "inizio_storia": "",
                "fine_storia": "",
            }
        )
    wb.close()
    return out


def extract_storici(xlsx: bytes) -> list[dict]:
    from openpyxl import load_workbook

    wb = load_workbook(io.BytesIO(xlsx), read_only=True, data_only=True)
    ws = _sheet_by_keyword(wb, "ccnl", "elenco")
    if ws is None:
        data_sheets = [s for s in wb.sheetnames if "guida" not in s.lower()]
        if not data_sheets:
            raise RuntimeError(f"Nessun foglio dati. Sheets: {wb.sheetnames}")
        ws = wb[data_sheets[0]]

    rows_iter = ws.iter_rows(values_only=True)
    header = [_norm(h).lower() for h in (next(rows_iter) or ())]
    idx = _header_index(header)

    def col(*frags: str) -> int | None:
        for i, h in enumerate(header):
            if all(f in h for f in frags):
                return i
        return None

    i_from = col("confluito", "cod")
    i_to = col("vigente", "cod")
    i_t_from = col("confluito", "titolo")
    i_t_to = col("vigente", "titolo")
    i_at = col("sezione", "ateco")
    i_atd = col("sezione", "ateco", "desc")
    i_start = col("inizio")
    i_end = col("fine")
    if i_from is None:
        raise RuntimeError(f"Colonne storici non riconosciute: {header}")

    out: list[dict] = []
    for row in rows_iter:
        if row is None:
            continue
        code_from = _norm(row[i_from]) if i_from < len(row) else ""
        if not code_from:
            continue
        out.append(
            {
                "fonte": "principali_storici",
                "codice_confluito": code_from,
                "confluenze_intermedie": "",
                "codice_vigente": _norm(row[i_to]) if i_to is not None and i_to < len(row) else "",
                "titolo_confluito": _norm(row[i_t_from]) if i_t_from is not None and i_t_from < len(row) else "",
                "titolo_vigente": _norm(row[i_t_to]) if i_t_to is not None and i_t_to < len(row) else "",
                "sezione_ateco": _norm(row[i_at]) if i_at is not None and i_at < len(row) else "",
                "sezione_ateco_desc": _norm(row[i_atd]) if i_atd is not None and i_atd < len(row) else "",
                "inizio_storia": _date(row[i_start]) if i_start is not None and i_start < len(row) else "",
                "fine_storia": _date(row[i_end]) if i_end is not None and i_end < len(row) else "",
            }
        )
    wb.close()
    return out


def main(out_path: Path) -> None:
    rows: list[dict] = []
    rows.extend(extract_confluenze_riepilogativo(download(RIEPILOGATIVO_URL)))
    rows.extend(extract_storici(download(STORICI_URL)))
    out_path.parent.mkdir(parents=True, exist_ok=True)
    with open(out_path, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=COLUMNS)
        writer.writeheader()
        writer.writerows(rows)
    print(f"Totale: {len(rows)} righe -> {out_path}")


if __name__ == "__main__":
    dest = Path(sys.argv[1]) if len(sys.argv) > 1 else Path("raw.csv")
    main(dest)
