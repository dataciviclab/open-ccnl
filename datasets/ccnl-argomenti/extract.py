#!/usr/bin/env python3
"""Sweep dell'Analisi Avanzata CNEL: accordi × sotto-argomenti (88 voci).

Per ogni sotto-argomento della tassonomia ufficiale (TE1 minimi, CR5 TFR, ...)
paginla ricerca pubblica e raccoglie gli accordi classificati.

Uso: python3 extract.py raw.csv
"""

from __future__ import annotations

import csv
import json
import sys
import time
import urllib.error
import urllib.request
from pathlib import Path

BASE = "https://az-apim-cne-sa-0002-lgc-we.azure-api.net/ricerca-api"

PAGE_SIZE = 200
SLEEP_S = 0.15
MAX_RETRIES = 3

COLUMNS = [
    "id_accordo",
    "codice_ccnl",
    "codice_argomento",
    "nome_argomento",
    "codice_macro",
    "nome_macro",
    "tipologia_accordo",
    "data_stipula",
    "data_decorrenza",
    "data_scadenza_contrattuale",
    "titolo_ccnl",
    "settori_ateco",
    "stato_aa",
    "ultimo_accordo_vigente",
]


def _request(path: str, body: dict | None = None, timeout: int = 60) -> dict:
    data = json.dumps(body).encode("utf-8") if body is not None else None
    req = urllib.request.Request(
        BASE + path,
        data=data,
        headers={"Content-Type": "application/json"} if data else {},
        method="POST" if data is not None else "GET",
    )
    last: Exception | None = None
    for attempt in range(MAX_RETRIES):
        try:
            with urllib.request.urlopen(req, timeout=timeout) as resp:
                return json.loads(resp.read().decode("utf-8"))
        except (urllib.error.URLError, urllib.error.HTTPError, TimeoutError) as e:
            last = e
            time.sleep(1.5 * (attempt + 1))
    raise RuntimeError(f"request fallita dopo {MAX_RETRIES} tentativi: {path}: {last}")


def taxonomy() -> list[dict]:
    """Ritorna i 88 sotto-argomenti con il parent (codice, nome)."""
    parents = _request("/tpl/ricerca/accordi/argomento/parent").get("list") or []
    out: list[dict] = []
    for p in parents:
        kids = (
            _request(f"/tpl/ricerca/accordi/argomento/{p['id']}/sotto-argomento").get("list")
            or []
        )
        for k in kids:
            out.append(
                {
                    "codice": k["codice"],
                    "nome": k.get("nome") or "",
                    "codice_macro": p.get("codice") or "",
                    "nome_macro": p.get("nome") or "",
                }
            )
    return out


def sweep_argomento(codice: str) -> list[dict]:
    """Pagina la ricerca AA per un sotto-argomento (tutte le stesure)."""
    rows: list[dict] = []
    page = 0
    while True:
        d = _request(
            "/ricerca/pubblica/accordi/cerca/accordi/aa",
            {
                "pageNumber": page,
                "pageSize": PAGE_SIZE,
                "sortBy": "dataStipula",
                "sortDesc": True,
                "codiciArgomenti": [codice],
                "codiceCcnl": None,
                "tipologiaAccordo": None,
                "statoAA": None,
                "settori": [],
                "regione": [],
                "provincia": [],
            },
        )
        pl = d.get("pagedList") or {}
        content = pl.get("content") or []
        rows.extend(content)
        total = int(pl.get("totalElements") or 0)
        page += 1
        if not content or len(rows) >= total:
            break
        time.sleep(SLEEP_S)
    return rows


def _trim_date(value: object) -> str:
    if not value:
        return ""
    return str(value)[:10]


def row_from_api(item: dict, tax: dict) -> dict:
    return {
        "id_accordo": item.get("idAccordo"),
        "codice_ccnl": (item.get("codiceCcnl") or "").strip().upper(),
        "codice_argomento": tax["codice"],
        "nome_argomento": tax["nome"],
        "codice_macro": tax["codice_macro"],
        "nome_macro": tax["nome_macro"],
        "tipologia_accordo": item.get("tipologiaAccordo") or "",
        "data_stipula": _trim_date(item.get("dataStipula")),
        "data_decorrenza": _trim_date(item.get("dataDecorrenza")),
        "data_scadenza_contrattuale": _trim_date(item.get("dataScadenzaContrattuale")),
        "titolo_ccnl": item.get("titoloCcnl") or "",
        "settori_ateco": ";".join(item.get("settoriAtecoAccordo") or []),
        "stato_aa": item.get("statoAA") or "",
        "ultimo_accordo_vigente": "true" if item.get("ultimoAccordoVigente") else "false",
    }


def main(out_path: Path) -> None:
    tax = taxonomy()
    print(f"Taxonomy: {len(tax)} sotto-argomenti", flush=True)

    seen: set[tuple[int, str]] = set()
    rows: list[dict] = []
    for i, t in enumerate(tax, 1):
        items = sweep_argomento(t["codice"])
        n_new = 0
        for item in items:
            key = (int(item.get("idAccordo") or 0), t["codice"])
            if key[0] <= 0 or key in seen:
                continue
            seen.add(key)
            rows.append(row_from_api(item, t))
            n_new += 1
        print(
            f"[{i}/{len(tax)}] {t['codice']}: {len(items)} righe, {n_new} nuove",
            flush=True,
        )

    out_path.parent.mkdir(parents=True, exist_ok=True)
    with open(out_path, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=COLUMNS)
        writer.writeheader()
        writer.writerows(rows)
    print(f"Totale: {len(rows)} righe -> {out_path}", flush=True)


if __name__ == "__main__":
    dest = Path(sys.argv[1]) if len(sys.argv) > 1 else Path("raw.csv")
    main(dest)
