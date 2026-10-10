# Note — ccnl-confluenze

- Excel verificati 2026-10-09.
- Header colonne storici: "CCNL confluito - cod", "CCNL vigente in cui è confluito - cod", ecc.
- Join utile: `codice_vigente` → `ccnl-metadata.codice_ccnl` / `ccnl-applicazione.codice_ccnl`.
- **Deroga PK clean**: `(fonte, codice_confluito)` non è univoco in fonte (righe multiple per storia/sezione). Il mart dedupa con `row_number` prioritizando `documento_riepilogativo`.
