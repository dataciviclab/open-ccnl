# ccnl-confluenze

Grafo storico: quali codici CCNL sono confluiti in quali contratti vigenti.

## Fonti

- Excel `documento-riepilogativo-testi-depositati.xlsx` (foglio confluenze)
- Excel `principali-ccnl-storici.xlsx` (elenco con date storia + titoli)

## Output

- **clean**: unione delle due fonti con colonna `fonte`
- **mart_ccnl_confluenze**: 1 riga = un codice confluito → codice vigente
  (priorità al documento riepilogativo)
