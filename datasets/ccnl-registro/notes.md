# ccnl-registro

Registro piatto dei CCNL/AEC depositati al CNEL: una riga per codice, con
status reale, tipo, sottosezione e firmatari normalizzati.

## Fonte

`documento-riepilogativo-testi-depositati.xlsx`, foglio **`1 - tutti i codici`**
(aggiornamento CNEL: 2026-10-31). È lo stesso file delle confluenze, ma il
foglio 1 non era usato.

## Output

- **clean**: 1 riga = 1 codice (`codice_ccnl`), 1.659 righe.
- **mart_ccnl_registro**: una riga per codice con flag booleani, conteggio
  firmatari e classificazioni (`is_aec`, `is_parasubordinato`,
  `is_nuovo_deposito`, `is_pubblico`, `is_dirigenti_privato`).
- **mart_firmatari_stats**: una riga per confederazione×tipo con numero di
  codici firmati, % sul totale, vigenti, dipendenti/AEC/parasubordinati.

## Cave

- Il campo `status` qui è quello reale (`vigente`/`confluito`/`cessato`);
  nell’API open data `stato` è sempre `acquisito`.
- I flag sono Sì/No della fonte, normalizzati a booleani. 22 codici hanno
  flag nulli (in genere depositi nuovi/minori).
- **I flag sono storici**: indicano che la confederazione ha firmato **almeno
  una stesura** del codice, non necessariamente il testo/ultimo deposito.
  Esempio: H011/C011/H05Y hanno `UGL = Sì`, ma la stringa
  `firmatari_sindacali` dell’ultimo deposito non elenca UGL.
- La stringa `firmatari_datoriali/sindacali` è l’ultimo deposito e resta il
  riferimento per “chi firma il testo corrente”; i flag servono per “chi ha
  firmato almeno una volta”. Non usare i flag come firmatari correnti.
- Un codice può avere più firmatari: le somme per confederazione non sono una
  partizione e possono superare il totale.
- **42 AEC + 19 parasubordinati** sono nel registro ma non hanno teste
  Uniemens (agenti/collaboratori non sono dipendenti): 58 codici a 0
  dipendenti, 3 ACN con ~83k.
- Gli 11 codici “catch-all” 2025–2026 sono tutti `CCNL di nuovo deposito`,
  con i grandi firmatari a `No` (solo H566/H185 hanno UGL).
- `n_firmatari_*` conta le voci separate da `;` nella stringa fonte: è un
  indicatore, non una validazione legale.
