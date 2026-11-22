# Note — ccnl-confluenze

- Excel verificati 2026-10-09.
- Header colonne storici: "CCNL confluito - cod", "CCNL vigente in cui è confluito - cod", ecc.
- **2026-11-22**: il file `principali-ccnl-storici.xlsx` ha cambiato header
  (`CCNL id confluito` / `CCNL id vigente`). L'extract ora riconosce entrambe
  le varianti (test in `tests/test_extract_logic.py`).
- Join utile: `codice_vigente` → `ccnl-metadata.codice_ccnl` / `ccnl-applicazione.codice_ccnl`.
- **Deroga PK clean**: `(fonte, codice_confluito)` non è univoco in fonte (righe multiple per storia/sezione). Il mart dedupa con `row_number` prioritizando `documento_riepilogativo`.
