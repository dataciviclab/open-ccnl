#!/usr/bin/env python3
"""Scarica l'anagrafica CCNL dall'API open data CNEL e la espone come CSV.

Fonte: API Azure APIM CNEL (nessuna auth).
- type=ARCHIVIO_CORRENTE  → accordi vigenti/ultrattivi
- type=ARCHIVIO_STORICO   → stesure storiche

Uso: python3 extract.py raw.csv
"""

from __future__ import annotations

import csv
import json
import sys
import urllib.request
from pathlib import Path

API_BASE = (
    "https://az-apim-cne-sa-0002-lgc-we.azure-api.net"
    "/ricerca-api/ricerca/pubblica/open-data"
)
TYPES = ("ARCHIVIO_CORRENTE", "ARCHIVIO_STORICO")

# Colonne piatte nel CSV (liste → stringa con ";").
COLUMNS = [
    "archivio",
    "id_accordo",
    "id_ccnl",
    "codice_ccnl",
    "identificativo_accordo",
    "ambito",
    "tipologia_accordo",
    "titolo",
    "titolo_ccnl",
    "stato",
    "stato_aa",
    "data_stipula",
    "data_decorrenza",
    "data_scadenza_contrattuale",
    "data_scadenza_economica",
    "data_pubblicazione",
    "ultimo_accordo_vigente",
    "visibile_online",
    "parti_datoriali",
    "parti_sindacali",
    "settori",
    "settori_descrizione",
    "settori_ateco",
    "settori_ateco_descrizione",
    "sottosettori_descrizione",
]


def _join(value: object) -> str:
    if value is None:
        return ""
    if isinstance(value, list):
        return ";".join(str(v).strip() for v in value if v is not None and str(v).strip())
    if isinstance(value, bool):
        return "true" if value else "false"
    return str(value).strip()


def fetch_type(type_name: str) -> list[dict]:
    url = f"{API_BASE}?type={type_name}"
    print(f"  fetch {type_name} ...", end=" ", flush=True)
    with urllib.request.urlopen(url, timeout=120) as resp:
        payload = json.loads(resp.read().decode("utf-8"))
    data = payload.get("data") if isinstance(payload, dict) else payload
    if not isinstance(data, list):
        raise RuntimeError(f"Risposta inattesa per {type_name}: {type(payload)}")
    print(f"{len(data)} righe")
    return data


def to_row(archivio: str, rec: dict) -> dict:
    return {
        "archivio": archivio,
        "id_accordo": _join(rec.get("idAccordo")),
        "id_ccnl": _join(rec.get("idCcnl")),
        "codice_ccnl": _join(rec.get("codiceCcnl")),
        "identificativo_accordo": _join(rec.get("identificativoAccordo")),
        "ambito": _join(rec.get("ambito")),
        "tipologia_accordo": _join(rec.get("tipologiaAccordo")),
        "titolo": _join(rec.get("titolo")),
        "titolo_ccnl": _join(rec.get("titoloCcnl")),
        "stato": _join(rec.get("stato")),
        "stato_aa": _join(rec.get("statoAA")),
        "data_stipula": _join(rec.get("dataStipula")),
        "data_decorrenza": _join(rec.get("dataDecorrenza")),
        "data_scadenza_contrattuale": _join(rec.get("dataScadenzaContrattuale")),
        "data_scadenza_economica": _join(rec.get("dataScadenzaEconomica")),
        "data_pubblicazione": _join(rec.get("dataPubblicazione")),
        "ultimo_accordo_vigente": _join(rec.get("ultimoAccordoVigente")),
        "visibile_online": _join(rec.get("visibileOnline")),
        "parti_datoriali": _join(rec.get("partiDatorialiFirmatarie")),
        "parti_sindacali": _join(rec.get("partiSindacaliFirmatarie")),
        "settori": _join(rec.get("settori")),
        "settori_descrizione": _join(rec.get("settoriDescrizione")),
        "settori_ateco": _join(rec.get("settoriAteco")),
        "settori_ateco_descrizione": _join(rec.get("settoriAtecoDescrizione")),
        "sottosettori_descrizione": _join(rec.get("sottosettoriDescrizione")),
    }


def main(out_path: Path) -> None:
    rows: list[dict] = []
    for type_name in TYPES:
        for rec in fetch_type(type_name):
            rows.append(to_row(type_name, rec))

    out_path.parent.mkdir(parents=True, exist_ok=True)
    with open(out_path, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=COLUMNS)
        writer.writeheader()
        writer.writerows(rows)
    print(f"Totale: {len(rows)} righe -> {out_path}")


if __name__ == "__main__":
    dest = Path(sys.argv[1]) if len(sys.argv) > 1 else Path("raw.csv")
    main(dest)
