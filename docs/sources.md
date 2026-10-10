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
