# ccnl-registro

Registro CNEL dei CCNL/AEC: status, tipo, sottosezione e firmatari
normalizzati, una riga per codice.

## Fonte

`documento-riepilogativo-testi-depositati.xlsx` — foglio
**`1 - tutti i codici`** (aggiornamento 2026-10-31).
Licenza dati: Italian Open Data License v2.0.

## Output

| Tabella | Grano |
|---|---|
| `clean` | `codice_ccnl` — 1.659 codici |
| `mart_ccnl_registro` | `codice_ccnl` + flag firmatari e classificazioni |
| `mart_firmatari_stats` | `confederazione` × `tipo` |

## Perché serve

L’API open data non dà lo status reale (sempre `acquisito`) né i firmatari in
forma normalizzata. Questo foglio colma il buco:
- `status`: 1.177 vigente, 296 confluito, 186 cessato;
- `tipo`: 1.598 dipendenti, 42 AEC, 19 parasubordinati;
- flag per Confindustria, Confapi, Confcommercio, Confesercenti,
  Confartigianato/CNA/Casa, Legacoop/Confcooperative/AGCI, CGIL/CISL/UIL,
  Confsal, Cisal, UGL.

Join consigliato: `codice_ccnl` con `ccnl-metadata`, `ccnl-applicazione` e
`mart_ccnl_classifica` (compose `mart_ccnl_intelligence` e
`mart_ccnl_firmatari`).

## Cave

- I flag sono **storici**: “almeno una stesura firmata”, non il testo corrente.
  La stringa `firmatari_*` è l’ultimo deposito e può non coincidere coi flag.
- Le quote per confederazione non sono una partizione: un codice può avere più
  firmatari e la somma può superare il 100%.
- 42 AEC + 19 parasubordinati sono nel registro ma non hanno teste Uniemens.
