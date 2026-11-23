#!/usr/bin/env python3
"""Scarica il "documento riepilogativo" CNEL e ne estrae il foglio
"1 - tutti i codici": registro piatto di 1.659 CCNL/AEC con status, tipo,
sottosezione e firmatari normalizzati.

Uso: python3 extract.py raw.csv
"""

from __future__ import annotations

import csv
import io
import sys
import urllib.request
from pathlib import Path

EXCEL_URL = (
    "https://www.cnel.it/media/docs/default-source/"
    "archivio-contratti---cartelle-excel/"
    "documento-riepilogativo-testi-depositati.xlsx"
)

COLUMNS = [
    "codice_ccnl",
    "sottosezione",
    "status",
    "tipo_ccnl",
    "titolo",
    "firmatari_datoriali",
    "firmatari_sindacali",
    "firmatari_sindacali_tavolo_separato",
    "firmatari_sindacali_adesione",
    "is_dirigenti",
    "confindustria",
    "confapi",
    "confcommercio",
    "confesercenti",
    "confartigianato_cna_casa",
    "legacoop_confcooperative_agci",
    "cgil_cisl_uil",
    "confsal",
    "cisal",
    "ugl",
]

# colonna sorgente (header normalizzato) → colonna output
SOURCE_COLUMNS = {
    "ccnl id": "codice_ccnl",
    "settore privato - sottosezione": "sottosezione",
    "status": "status",
    "tipo ccnl": "tipo_ccnl",
    "ccnl titolo": "titolo",
    "firmatari datoriali": "firmatari_datoriali",
    "firmatari sindacali": "firmatari_sindacali",
    "firmatari sindacali su tavolo separato con i soli datoriali": "firmatari_sindacali_tavolo_separato",
    "firmatari sindacali per adesione con i soli datoriali": "firmatari_sindacali_adesione",
    "dirigenti": "is_dirigenti",
    "confindustria": "confindustria",
    "confapi": "confapi",
    "confcommercio": "confcommercio",
    "confesercenti": "confesercenti",
    "confartigianato cna casa": "confartigianato_cna_casa",
    "legacoop confcooperative agci": "legacoop_confcooperative_agci",
    "cgil cisl uil": "cgil_cisl_uil",
    "confsal": "confsal",
    "cisal": "cisal",
    "ugl": "ugl",
}

FLAG_COLUMNS = {
    "is_dirigenti",
    "confindustria",
    "confapi",
    "confcommercio",
    "confesercenti",
    "confartigianato_cna_casa",
    "legacoop_confcooperative_agci",
    "cgil_cisl_uil",
    "confsal",
    "cisal",
    "ugl",
}


def _norm(value: object) -> str:
    if value is None:
        return ""
    return " ".join(str(value).split())


def _flag(value: object) -> str:
    text = _norm(value).lower()
    if text in {"sì", "si", "s", "true", "1", "yes"}:
        return "true"
    if text in {"no", "false", "0"}:
        return "false"
    return ""


def download_xlsx() -> bytes:
    print(f"  download {EXCEL_URL}", flush=True)
    req = urllib.request.Request(
        EXCEL_URL, headers={"User-Agent": "dataciviclab-open-ccnl/0.1"}
    )
    with urllib.request.urlopen(req, timeout=180) as resp:
        data = resp.read()
    print(f"  {len(data)} bytes")
    return data


def extract_registro(xlsx_bytes: bytes) -> list[dict]:
    from openpyxl import load_workbook

    wb = load_workbook(io.BytesIO(xlsx_bytes), read_only=True, data_only=True)
    candidates = [s for s in wb.sheetnames if "tutti i codici" in s.lower()]
    if not candidates:
        raise RuntimeError(
            f"Foglio '1 - tutti i codici' non trovato. Sheets: {wb.sheetnames}"
        )
    ws = wb[candidates[0]]

    rows_iter = ws.iter_rows(values_only=True)
    header = [_norm(h).lower() for h in (next(rows_iter) or ())]
    idx = {h: i for i, h in enumerate(header) if h}

    missing = [src for src in SOURCE_COLUMNS if src not in idx]
    if missing:
        raise RuntimeError(f"Colonne registro non riconosciute: {missing}. Header: {header}")

    out: list[dict] = []
    for row in rows_iter:
        if row is None:
            continue
        code = _norm(row[idx["ccnl id"]]).upper()
        if not code:
            continue
        record: dict[str, str] = {}
        for src, dst in SOURCE_COLUMNS.items():
            j = idx[src]
            value = row[j] if j < len(row) else None
            record[dst] = _flag(value) if dst in FLAG_COLUMNS else _norm(value)
        out.append(record)

    wb.close()
    return out


def main(out_path: Path) -> None:
    rows = extract_registro(download_xlsx())
    out_path.parent.mkdir(parents=True, exist_ok=True)
    with open(out_path, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=COLUMNS)
        writer.writeheader()
        writer.writerows(rows)
    print(f"Totale: {len(rows)} righe -> {out_path}")


if __name__ == "__main__":
    dest = Path(sys.argv[1]) if len(sys.argv) > 1 else Path("raw.csv")
    main(dest)
