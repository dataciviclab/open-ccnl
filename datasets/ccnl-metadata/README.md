# ccnl-metadata

Anagrafica dei CCNL depositati presso l'Archivio CNEL.

## Fonte

API open data CNEL (Azure APIM), tipi `ARCHIVIO_CORRENTE` e `ARCHIVIO_STORICO`.
Aggiornamento: settimanale lato CNEL. Nessuna autenticazione.

## Output

- **clean**: 1 riga = 1 accordo depositato (`id_accordo` × `archivio`)
- **mart_ccnl_codici**: 1 riga = un codice CCNL con conteggio stesure e range date

## Vincoli noti

- Il campo `dipendenti` dell'API è quasi sempre `null` → metriche in `ccnl-applicazione`.
- Non contiene i testi dei contratti (PDF scaricabili via endpoint dedicato, non in v0).
