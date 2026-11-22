# ccnl-metadata

Anagrafica dei CCNL depositati presso l'Archivio CNEL.

## Fonte

API open data CNEL (Azure APIM), tipi `ARCHIVIO_CORRENTE` e `ARCHIVIO_STORICO`.
Aggiornamento: settimanale lato CNEL. Nessuna autenticazione.

## Output

- **clean**: 1 riga = 1 accordo depositato (`id_accordo` × `archivio`)
- **mart_ccnl_codici**: 1 riga = un codice CCNL con conteggio stesure e range date
- **mart_ccnl_ateco**: codice × sezione ATECO
- **mart_ccnl_rinnovi**: ultimo accordo per codice (tutte le tipologie) con
  scadenza, giorni di ritardo e flag `scaduto`

## Vincoli noti

- Il campo `dipendenti` dell'API è quasi sempre `null` → metriche in `ccnl-applicazione`.
- Non contiene i testi dei contratti (PDF scaricabili via endpoint dedicato, non in v0).
- `stato` è sempre `acquisito`; `ultimo_accordo_vigente` è true su tutto il corrente.
- Copertura: 2 tipi di archivio su 10 (~42k accordi non ingeriti).
