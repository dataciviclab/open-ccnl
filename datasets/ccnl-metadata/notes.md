# Note — ccnl-metadata

- API verificata 2026-10-09: ARCHIVIO_CORRENTE ~2287 righe, ARCHIVIO_STORICO ~5398.
- `dipendenti` / `comparto` / `sezione` sempre null nel JSON open data.
- `settori_ateco` presente in ~99% del corrente, ~60% dello storico.
- Join utile con `ccnl-applicazione` su `codice_ccnl`.
- **`stato` è sempre `acquisito`**: non è lo status del contratto. Lo status
  utile è `ccnl_applicazione.status` (`vigente`/`confluito`/`cessato`).
- **`ultimo_accordo_vigente` è true su tutte le righe dell'archivio corrente**:
  significa "in vigore", non "ultimo". Per l'ultimo accordo usare
  `mart_ccnl_rinnovi`.
- Copertura: 2 tipi di archivio su 10 (mancano ~42k accordi interconfederali,
  quadro, solidarietà, ARAN decentrati).
