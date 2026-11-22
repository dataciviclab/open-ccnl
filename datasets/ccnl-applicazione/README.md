# ccnl-applicazione

Metriche di applicazione reale dei CCNL (INPS Uniemens + conto annuale PPAA).

## Fonte

Excel open data CNEL `dati-sull'applicazione-dei-ccnl-dal-2018.xlsx`,
foglio `1 - dati quantitativi`. Fogli provinciali in `ccnl-territorio`.

## Output

- **clean / mart**: 1 riga = `codice_ccnl` × `anno` (2018–2025)
- Colonne: `n_datori`, `n_dipendenti`, `n_dipendenti_f/m` (dal 2023, solo privato)
- `is_conto_annuale_ppaa`: marca i codici PA (Conto Annuale RGS)

## Mart

| Mart | Uso |
|---|---|
| `mart_ccnl_serie` | serie lunga, quote, rank per anno, `pa_inclusa` |
| `mart_ccnl_top` | ultimo dato per codice (anni misti: leggere `ultimo_anno_con_dati`) |
| `mart_ccnl_classifica` | classifica omogenea sull'ultimo anno con PA (2024) |
| `mart_ccnl_mercati` | sottosezione × anno |
| `mart_ccnl_totali_anno` | totali onesti per anno + quote donne |

## Cave

- PA: la fonte lascia 0 nel 2025 (Conto Annuale non disponibile). `pa_inclusa`
  segnala gli anni confrontabili.
- H501 (domestico): serie che parte nel 2025; il salto datori è perimetro.
- Genere: F/M solo Uniemens; PA e H501 hanno quota `NULL` (non 0).
- 2025 è completo per il privato, non per il totale Italia.
