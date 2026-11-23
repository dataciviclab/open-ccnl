# ccnl-analisi (compose)

Join analitico dei dataset sibling in quattro mart pronti all’uso.

## Support

| name | dataset | mart usati |
|---|---|---|
| applicazione | `datasets/ccnl-applicazione` | `mart_ccnl_top`, `mart_ccnl_classifica` |
| metadata | `datasets/ccnl-metadata` | `mart_ccnl_codici`, `mart_ccnl_ateco` |
| confluenze | `datasets/ccnl-confluenze` | `mart_ccnl_vigenti_confluenze` |
| registro | `datasets/ccnl-registro` | `mart_ccnl_registro` |

## Mart

### `mart_ccnl_intelligence`
1 riga = 1 codice CCNL con:
- peso Uniemens (ultimo dato disponibile, rank, quota, Δ)
- classifica omogenea sull'ultimo anno con PA (`anno_riferimento`,
  `rank_nazionale`, `quota_dipendenti`)
- anagrafica depositi (stesure, vita)
- ATECO aggregati
- n. storie confluite
- status/tipo/sottosezione e firmatari dal registro CNEL
- fascia_peso (A ≥1M … F)

### `mart_ccnl_settori`
1 riga = codice × sezione ATECO (per join settoriali).  
Il `n_dipendenti` è del CCNL intero, non ripartito per divisione.

### `mart_ccnl_geo`
Top 5 province dei top 30 CCNL, sullo stesso `anno_riferimento` della
classifica. La PA non ha dettaglio provinciale in questa fonte.

### `mart_ccnl_firmatari`
Peso 2024 per confederazione firmataria (Confindustria, Confapi,
Confcommercio, Confesercenti, Confartigianato/CNA/Casa,
Legacoop/Confcooperative/AGCI, CGIL/CISL/UIL, Confsal, Cisal, UGL).
I flag sono **storici** (almeno una stesura firmata), non il testo corrente;
le quote non sono una partizione e possono superare il 100%.

## Run

```bash
make run   # include compose dopo i datasets (ordine alfabetico: compose prima!)
# meglio:
TOOLKIT_ALLOW_SCRIPT_SOURCE=1 toolkit run --config datasets/ccnl-applicazione/dataset.yml
# ... gli altri due ...
toolkit run --config compose/ccnl-analisi/dataset.yml
```

Il compose riusa gli output già presenti in `out/` (skip-if-exists dei support).
