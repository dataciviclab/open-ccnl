# ccnl-argomenti — note

## Fonte

API pubblica CNEL **Analisi Avanzate** (stessa base Azure APIM dell'open data):

- `GET /tpl/ricerca/accordi/argomento/parent` — 14 macro-argomenti
- `GET /tpl/ricerca/accordi/argomento/{id}/sotto-argomento` — 88 sotto
- `POST /ricerca/pubblica/accordi/cerca/accordi/aa` — ricerca paginata per
  codice sotto-argomento (`codiciArgomenti: ["TE1"]`; i codici parent non
  restituiscono risultati)

Sweep: 88 ricerche paginate (pageSize 200, ~0.15s di pausa) → tutte le stesure
classificate su ciascun argomento. Runtime atteso 1-3 minuti.

## Perimetro e limiti

- **4.812 accordi** con AA pubblicata (non tutti i ~7.700 depositi in anagrafica).
- Classificazione su **tutte le stesure**, non solo testi definitivi:
  un codice può comparire N volte (es. H011: decine di versioni).
- Dettagli per-accordo (html/tree clausole) sono back-office, non open:
  qui arriva la **presenza** dell'argomento, non il testo della clausola.
- Stessa classe di stabilità dell'API open data CNEL (documentare in
  source-check `cnel.it`).

## Mapping con i nostri 28 istituti (corpus)

Il vocabolario regex del corpus documentale (branch
`sperimentale/corpus-docs`) mappa ogni istituto ai codici AA
(`ccnl_istituti_cnel_map.parquet`). Perimetro diverso: regex = ultimo testo
definitivo; AA = tutte le stesure. Non è contraddizione, è copertura.
