# open-ccnl

[![ci](https://github.com/dataciviclab/open-ccnl/actions/workflows/ci.yml/badge.svg)](https://github.com/dataciviclab/open-ccnl/actions/workflows/ci.yml)
[![license: MIT](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)

**I Contratti Collettivi Nazionali dell'Italia, in dati aperti.** In Italia
circa 8 lavoratori su 10 lavorano sotto un CCNL: sono le regole di stipendi,
tutele e orari per milioni di persone. Questo repo rende interrogabili
l'anagrafica nazionale CNEL, le metriche di applicazione Uniemens/INPS e il
grafo delle confluenze tra contratti.

## Cosa contengono i dati

| Dataset | Righe | Periodo | Contenuto |
|---|---:|---|---|
| `ccnl_metadata` | ~7.700 | storico + corrente | Accordi depositati: codici, date, firmatari, ATECO |
| `ccnl_applicazione` | ~13.200 | 2018–2025 | Datori e dipendenti per CCNL × anno (F/M dal 2023) |
| `ccnl_territorio` | ~166.000 | 2023–2025 | Dipendenti per provincia × genere × CCNL |
| `ccnl_confluenze` | ~610 | — | Mappa confluenze: quale codice storico è confluito dove |

+ 12 mart analitici (ranking nazionali, serie storiche, quote di genere,
intelligenza contrattuale composta). Fonte: [CNEL Archivio Contratti](https://www.cnel.it/archivio-contratti/contratti-open-data)
— Italian Open Data License v2.0.

## Esempi di domande

- Quali sono i 20 CCNL che coprono più dipendenti, e come sono cambiate le quote?
- Quanti contratti collettivi vigono in quali comparti, e dove è più frammentato?
- Quali CCNL hanno superato la scadenza contrattuale e quanti lavoratori restano sotto quelle regole?
- Come si sono fusi i codici contrattuali storici nei vigenti (grafo confluenze)?
- Quante donne e uomini copre ogni contratto, per provincia?

## Come accedere

1. **Parquet su GCS** — clean e mart esportati dal pipeline org; percorsi in
   [`registry/registry.json`](registry/registry.json)
   (`gs://dataciviclab-clean/` + duckdb httpfs).
2. **Locale** — `uv pip install -e ".[pipeline]" && make run` → parquet in `out/data/`.
3. **DuckDB diretto** — qualsiasi client che legga parquet del registry.

## Approfondimenti

- [Discussions del repo](https://github.com/dataciviclab/open-ccnl/discussions) — domande, idee, casi d'uso
- [Decisioni tecniche](docs/decisions.md) · [Fonti](docs/sources.md)

## Partecipa

Hai trovato un dato sbagliato o vuoi proporre un join con altri dataset del Lab?
Apri una [Discussion](https://github.com/dataciviclab/open-ccnl/discussions) o
un issue nel repo: contribuzioni di dati, SQL e segnalazioni sono benvenute
([CONTRIBUTING.md](CONTRIBUTING.md)).

## Note sui dati

- Il campo `dipendenti` dell'API JSON è quasi sempre `null`: le metriche stanno
  nell'Excel applicazione (Uniemens + conto annuale PPAA per la PA).
- Alcuni CCNL PA hanno dipendenti Uniemens = 0: il dato è sul conto annuale.
- 2025 può essere parziale (media 12 mesi a chiusura estrazione).
- F012 (edili): il CNEL deposita solo accordi di rinnovo, niente testo definitivo.

## Sviluppo

```bash
uv pip install -e ".[pipeline,dev]" --system
make check   # preflight config
make run     # scarica + clean + mart
make test    # contratti config + logica extract
```

Licenza del codice: [MIT](LICENSE). Licenza dei dati CNEL: IODL v2.0.
