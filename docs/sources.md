# Fonti CNEL — riferimenti

## API open data (metadata)

Base:

```
https://az-apim-cne-sa-0002-lgc-we.azure-api.net/ricerca-api/ricerca/pubblica/open-data?type=<TYPE>
```

Tipi utilizzati in v0:

| type | Contenuto (2026-10) |
|---|---|
| `ARCHIVIO_CORRENTE` | ~2287 accordi vigenti/ultrattivi |
| `ARCHIVIO_STORICO` | ~5398 stesure storiche |

Altri tipi disponibili (non in v0): ARAN decentrati, accordi Governo/parti sociali, quadro, interconfederali, solidarietà.

## Copertura archivio (verifica 2026-11-22)

| type | Accordi | In open-ccnl |
|---|---:|---|
| `ARCHIVIO_CORRENTE` | 2.331 | sì |
| `ARCHIVIO_STORICO` | 5.463 | sì |
| `ACCORDI_INTERCONFEDERALI` | 502 | no |
| `CONTRATTI_QUADRO` | 87 | no |
| `ACCORDI_GOVERNO_PARTI_SOCIALI` | 47 | no |
| `CONTRATTI_SOLIDARIETA` | 1.414 | no |
| `ARAN_DECENTRATI_PUBBLICO_NAZIONALE` | 2.155 | no |
| `PRE_ARAN_DECENTRATI_PUBBLICO` | 37.494 | no |
| `PRE_ARAN_DECENTRATI_PUBBLICO_NAZIONALE` | 281 | no |

I tipi non in v0 sono ~42k accordi: granularità e schema diversi (decentrato,
aziendale, interconfederale). Candidati a un dataset separato
(`ccnl_altri_accordi`), non a un'unione in `ccnl_metadata`.

Risposta: `{"data": [ ... ]}`. Campo `dipendenti` quasi sempre `null`.

## Excel metriche e grafo

Pagina: https://www.cnel.it/archivio-contratti/contratti-open-data

| File | Uso |
|---|---|
| `dati-sull'applicazione-dei-ccnl-dal-2018.xlsx` | foglio quantitativi + provinciali |
| `documento-riepilogativo-testi-depositati.xlsx` | tutti i codici + confluenze |
| `principali-ccnl-storici.xlsx` | storie con date + titoli |

## Download PDF testi (fuori v0)

```
GET .../ricerca/pubblica/accordi/scarica/accordi/{idAccordo}
→ JSON con fileContent (base64 PDF) + fileUrl blob (privato)
```

## Licenza

Italian Open Data License v2.0 — riproduzione con indicazione fonte.
