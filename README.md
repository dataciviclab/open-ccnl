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
| `ccnl_metadata` | ~7.800 | storico + corrente | Accordi depositati: codici, date, firmatari, ATECO |
| `ccnl_registro` | ~1.660 | 2026 | Registro CNEL: status, tipo, sottosezione, firmatari normalizzati |
| `ccnl_applicazione` | ~13.200 | 2018–2025 | Datori e dipendenti per CCNL × anno (F/M dal 2023, solo privato) |
| `ccnl_territorio` | ~166.000 | 2023–2025 | Dipendenti per provincia × genere × CCNL (solo Uniemens) |
| `ccnl_confluenze` | ~610 | — | Mappa confluenze: quale codice storico è confluito dove |

+ 22 mart analitici (ranking omogenei, serie storiche, quote di genere,
totali per anno, radar rinnovi, firmatari e intelligence contrattuale composta). Fonte:
[CNEL Archivio Contratti](https://www.cnel.it/archivio-contratti/contratti-open-data)
— Italian Open Data License v2.0.

## Esempi di domande

- Quali sono i 20 CCNL che coprono più dipendenti, e come sono cambiate le quote?
- Chi firma i CCNL che coprono più lavoratori, e quanta parte del privato è coperta dalle grandi confederazioni?
- Quanti contratti collettivi vigono in quali comparti, e dove è più frammentato?
- Quanti codici sono AEC o parasubordinati, e perché non hanno teste in Uniemens?
- Quali CCNL hanno superato la scadenza contrattuale e quanti lavoratori restano sotto quelle regole?
- Come si sono fusi i codici contrattuali storici nei vigenti (grafo confluenze)?
- Quante donne e uomini copre ogni contratto, per provincia?

## Universo dei dati (leggere prima dei totali)

- **2025 non è un anno completo**: la PA (codici `S*`, Conto Annuale RGS) non è
  ancora pubblicata. Nel 2025 il dataset nazionale copre solo Uniemens/privato
  (~15,7M); nel 2024 copre privato + PA (~18,1M). Usare il **2024** per totali,
  quote e confronti; il mart `mart_ccnl_classifica` è già ancorato all'ultimo
  anno con PA.
- **H501 lavoro domestico** compare solo dal 2025 (523k dipendenti e 523k
  datori): il salto dei datori nel 2025 è un cambio di perimetro, non crescita.
- **Genere**: F/M esiste solo per Uniemens (privato). La PA non ha dettaglio di
  genere in questa fonte: le quote sono `NULL`, non 0%. Per la PA usare
  `dipendenti_pubblici` (Conto Annuale, 60,2% donne nel 2024).
- **Territorio vs nazionale**: il territorio include aggregati non-CCNL
  (`CPUB`, `CDIV`) e non ha il dettaglio PA né H501; il nazionale include la PA
  ma non quei aggregati. I due totali non sono sommabili.
- **Registro firmatari**: i flag di `ccnl_registro` sono **storici** (almeno
  una stesura firmata), non i firmatari del testo corrente; la stringa
  `firmatari_*` è l'ultimo deposito. 42 AEC + 19 parasubordinati sono nel
  registro ma non hanno teste Uniemens; i 3 AEC con teste valgono 84.943
  dipendenti nel 2024. Cella vuota → `NULL`: 19 `CCNL di nuovo deposito`
  finiscono in `C_non_dichiarato`, non in “solo minori”.
- **Province**: la fonte usa la geografia pre-2016 (CI, OG, OT, VS) e include
  ESTERO.

Dettaglio in [`docs/decisions.md`](docs/decisions.md).

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
- I CCNL PA hanno dipendenti Uniemens = 0: il dato è nel Conto Annuale RGS.
  Nel 2025 il Conto Annuale non è disponibile: i codici `S*` sono a 0.
- H501 (lavoro domestico) è popolato solo dal 2025; prima il codice è a 0.
- F/M è disponibile solo per Uniemens (privato), dal 2023. PA e H501 non hanno
  genere in questa fonte: la quota è `NULL`, non 0%.
- `ccnl_argomenti` copre 81 dei 88 sotto-argomenti ufficiali (7 senza accordi
  classificati) e 4.602 accordi distinti (95.899 righe accordo×argomento), non
  tutti i ~7.800 depositi.
- F012 (edili): il CNEL deposita solo accordi di rinnovo, niente testo definitivo.

## Sviluppo

```bash
uv pip install -e ".[pipeline,dev]" --system
make check   # preflight config
make run     # scarica + clean + mart
make lint    # ruff
make test    # contratti config + logica extract + semantica mart
```

Licenza del codice: [MIT](LICENSE). Licenza dei dati CNEL: IODL v2.0.
