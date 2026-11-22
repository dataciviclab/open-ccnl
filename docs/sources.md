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

## Stato fonte 2026-11-22 (delta vs snapshot 2026-11-01)

- API metadata: **+77 accordi** (corrente +36, storico +41), **+13 codici**.
  Ultimo deposito: `S105` Funzioni Locali, **2026-10-28**.
- Accordi 2026 in anagrafica: **291** (222 nello snapshot). Sono 143 testi
  definitivi, 99 verbali, 35 rinnovi, 11 economici, 3 secondo biennio.
- Rimosso un accordo con `data_stipula = 2028-08-26` (`T279`): la fonte ha
  corretto una data futura.
- Excel applicazione: aggiornato al 2026-11-09, ma la colonna 2026 ha solo
  3 valori (`S241`, `S251`, `S261`). Metriche 2018–2025 invariate.
- Confluenze: header di `principali-ccnl-storici.xlsx` cambiato
  (`CCNL confluito - cod` → `CCNL id confluito`); l’extract gestisce entrambi.

### 11 nuovi codici senza metriche né confluenze

Sono nuovi `id_ccnl` (1779–1790), non alias di codici esistenti. Tutti
`Testo definitivo`, `stato_aa = Non Classificato`, con ATECO molto ampi:

| Codice | Primo deposito | ATECO | Datori | Sindacati |
|---|---|---|---|---|
| `V71D` | 2026-07-23 | 43 voci, quasi tutti i settori | CONFIMPRENDITORI | USIL/SUL/FILCOM |
| `V733` | 2026-05-20 | 22 voci manifatturiere | CIFA | CONFSAL |
| `H16N` | 2026-08-07 | 46;47;G | CONFIMPRENDITORI | USIL/SUL/FILCOM |
| `H184` | 2026-07-08 | 55;56;S;92;I;93 | CONFIMPRENDITORI | USIL/SUL/FILCOM |
| `H185` | 2026-07-23 | 55;56;S;92;I;93 | CONF.EUR.ASS.IMPRESE | UGL Terziario |
| `H566` | 2026-07-23 | U;97 (colf/badanti) | CONF.EUR.ASS.IMPRESE | UGL Terziario |
| `HV32` | 2026-09-08 | Q;C;26;F;85;43 | UNILAVORO PMI | CISALP/UGL |
| `I15B` | 2026-06-30 | 49;H | ITALPMI e altri | FESICA |
| `H457` | 2026-09-14 | R;86 (odontoiatria) | ASSOESERCENTI | CIU |
| `F08Z` | 2025-04-09 | F;41;42;43 (edilizia) | ITALPMI | UNSIL |
| `C05F` | 2025-09-22 | 33;24;C;25;28;29 | UNILAVORO PMI | CISALP |

Sono contratti “catch-all” depositati da associazioni datoriali minori: non
hanno dipendenti in Uniemens, non sono in AA e non hanno confluenze. Da
monitorare se entrano nell’Excel applicazione (rischio frammentazione).

### Analisi Avanzata ferma al 2023-06

- Ultimo accordo classificato: **2023-06-23**; 4.812 accordi, 95.899 righe.
- Accordi successivi in anagrafica: **1.039** su **630 codici**, che coprono
  **14,8M dipendenti** (2025) — il 94,6% del privato.
- Di questi 630 codici, **396 non hanno alcuna classificazione AA** e **234
  hanno AA più vecchia dell’ultimo accordo**: nessuno è aggiornato.
- Dei 241 codici con un accordo 2026, **171 non hanno AA** e **70 hanno AA
  vecchia**: zero aggiornati.

Conseguenza: `ccnl_argomenti` è una **mappa storica**, non una fotografia dei
contratti vigenti. Per i rinnovi 2024–2026 non ci sono tag AA.

## Download PDF testi (fuori v0)

```
GET .../ricerca/pubblica/accordi/scarica/accordi/{idAccordo}
→ JSON con fileContent (base64 PDF) + fileUrl blob (privato)
```

## Licenza

Italian Open Data License v2.0 — riproduzione con indicazione fonte.
