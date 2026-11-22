# ccnl-territorio

Dove si applicano i CCNL: **provincia × genere × anno** (INPS Uniemens).

## Fonte

Stesso Excel di `ccnl-applicazione`, fogli:
- `2-dati INPS 2023 provinc genere`
- `3-dati INPS 2024 provinc genere`
- `4 - dati INPS 2025 prov genere`

~55k righe/anno, 108 province, 21 regioni.  
Header colonna codice non stabile (`CODICE_CCNL` vs `CODICE_CONTRATTO`) → normalizzato in extract.

## Mart

| Mart | Grano |
|---|---|
| `mart_ccnl_provincia` | CCNL × anno × provincia (F/M, rank nella provincia) |
| `mart_ccnl_regione` | CCNL × anno × regione + n. provincie |
| `mart_provincia_sintesi` | provincia × anno (tutti i CCNL, F/M, n. codici) |

## Incastro con il resto

```
ccnl-applicazione.mart_ccnl_serie     → nazionale CCNL × anno
ccnl-territorio.mart_ccnl_provincia   → geografia dello stesso codice
ccnl-analisi.mart_ccnl_intelligence   → profilo pieno per codice
```

Join naturale: `(codice_ccnl, anno)`.

## Cave

- Uniemens ≠ conto annuale PA: il territorio non ha il dettaglio PA.
- `CPUB` e `CDIV` sono aggregati non-CCNL: non sommarli ai codici.
- H501 domestico: **assente** dal territorio (nessuna copertura geografica).
- 2025 è completo per il privato; la PA non è in questa fonte.
- Geografia pre-2016: `CI`, `OG`, `OT`, `VS` soppresse; `EE` = ESTERO.
- Griglia: righe sparse (non full cross product) — i 0 nel raw sono assenze reali/spurie
