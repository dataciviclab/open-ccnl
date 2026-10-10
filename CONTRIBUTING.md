# Contributing — open-ccnl

Repo dataset del Lab (`dataciviclab/open-ccnl`) per l'archivio nazionale CCNL
(CNEL). Le convenzioni canoniche sono in
[lab-ops](https://github.com/dataciviclab/lab-ops) — standard repo, test,
pipeline.

## Scope

- **In scope**: anagrafica CCNL (API open data CNEL), metriche Uniemens
  (Excel dati applicazione), territorio, confluenze, mart analitici.
- **Out of scope**: corpus PDF / OCR / estrazione clausole

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
- Gli Excel multi-sheet richiedono `type: script` + `extract.py` (non `http_file`);
  gli extract sono stdlib-only (urllib + csv), niente dipendenze Excel.
- Category chiusa: `welfare-lavoro` (candidate-standard App. A).
- Ogni test ha un marker (`contract` / `adapter` / `pure_unit` / `smoke`).

## CI

- `ci.yml`: test (`make test`) su push/PR + preflight config dataset sulle PR.
- `pipeline.yml`: run completo post-merge + refresh mensile (reusable org).

## Fonti

- API: `https://az-apim-cne-sa-0002-lgc-we.azure-api.net/ricerca-api/ricerca/pubblica/open-data`
- Excel: pagina [Contratti Open Data CNEL](https://www.cnel.it/archivio-contratti/contratti-open-data)
- Licenza dati: Italian Open Data License v2.0 (indicazione fonte obbligatoria)
