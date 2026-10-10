# Note — ccnl-metadata

- API verificata 2026-10-09: ARCHIVIO_CORRENTE ~2287 righe, ARCHIVIO_STORICO ~5398.
- `dipendenti` / `comparto` / `sezione` sempre null nel JSON open data.
- `settori_ateco` presente in ~99% del corrente, ~60% dello storico.
- Join utile con `ccnl-applicazione` su `codice_ccnl`.
