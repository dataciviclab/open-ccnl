# Contributing — open-ccnl

Repo sperimentale locale (`esperimenti-locali/`) per l'archivio CNEL dei CCNL.
Quando sarà promosso a repo Lab ufficiale, i contributing standard di
[`infra/lab-ops`](../../infra/lab-ops/) diventeranno canonici.

## Scope

- **In scope (v0)**: anagrafica CCNL (API open data CNEL), metriche Uniemens
  (Excel dati applicazione), grafo confluenze.
- **Out of scope (v0)**: corpus PDF / OCR / estrazione clausole — epica separata.

## Come girare la pipeline

```bash
# solo validazione config
make check

# run di tutti i dataset (scarica fonti reali)
make run

# singolo dataset
toolkit run --config datasets/ccnl-metadata/dataset.yml
```

Output in `out/` (non committare).

## Convenzioni

- `dataset.yml` è l'unica fonte di verità della pipeline.
- `clean.sql` legge solo da `raw_input`; `mart*.sql` solo da `clean_input`.
- Gli Excel multi-sheet richiedono `type: script` + `extract.py` (non `http_file`).
- Category chiusa: `welfare-lavoro` (candidate-standard App. A).
- Ogni test ha un marker (`contract` / `adapter` / `pure_unit` / `smoke`).

## Fonti

- API: `https://az-apim-cne-sa-0002-lgc-we.azure-api.net/ricerca-api/ricerca/pubblica/open-data`
- Download PDF: `.../accordi/scarica/accordi/{idAccordo}` (non in v0)
- Excel: pagina [Contratti Open Data CNEL](https://www.cnel.it/archivio-contratti/contratti-open-data)
