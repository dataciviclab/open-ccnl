# ccnl-analisi (compose)

Join analitico dei tre dataset sibling in due mart pronti all’uso.

## Support

| name | dataset | mart usati |
|---|---|---|
| applicazione | `datasets/ccnl-applicazione` | `mart_ccnl_top` |
| metadata | `datasets/ccnl-metadata` | `mart_ccnl_codici`, `mart_ccnl_ateco` |
| confluenze | `datasets/ccnl-confluenze` | `mart_ccnl_vigenti_confluenze` |

## Mart

### `mart_ccnl_intelligence`
1 riga = 1 codice CCNL con:
- peso Uniemens (ultimo anno, rank, quota, Δ)
- anagrafica depositi (stesure, vita)
- ATECO aggregati
- n. storie confluite
- fascia_peso (A ≥1M … F)

### `mart_ccnl_settori`
1 riga = codice × sezione ATECO (per join settoriali).  
Il `n_dipendenti` è del CCNL intero, non ripartito per divisione.

## Run

```bash
make run   # include compose dopo i datasets (ordine alfabetico: compose prima!)
# meglio:
TOOLKIT_ALLOW_SCRIPT_SOURCE=1 toolkit run --config datasets/ccnl-applicazione/dataset.yml
# ... gli altri due ...
toolkit run --config compose/ccnl-analisi/dataset.yml
```

Il compose riusa gli output già presenti in `out/` (skip-if-exists dei support).
