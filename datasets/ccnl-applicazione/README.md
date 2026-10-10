# ccnl-applicazione

Metriche di applicazione reale dei CCNL (INPS Uniemens + conto annuale PPAA).

## Fonte

Excel open data CNEL `dati-sull'applicazione-dei-ccnl-dal-2018.xlsx`,
foglio `1 - dati quantitativi`. Fogli provinciali (2023–2025) **non** in v0.

## Output

- **clean / mart**: 1 riga = `codice_ccnl` × `anno` (2018–2025)
- Colonne: `n_datori`, `n_dipendenti`, `n_dipendenti_f/m` (dal 2023)

## Cave

- PA: spesso Uniemens = 0; vedere `filtri_conto_annuale_ppaa`.
- H501 (domestico): serie non confrontabile pre-2025.
- 2025 può essere parziale a seconda della chiusura Uniemens.
