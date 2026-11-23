# Decisioni — open-ccnl

Registro pubblico e sintetico delle scelte che cambiano il contratto dei dati.
Le note operative più lunghe restano in `_local/decisions.md` (non versionato).

## 2026-11-23 — Registro CNEL (foglio “1 - tutti i codici”)

- **Decisione**: usare il foglio 1 di `documento-riepilogativo-testi-depositati.xlsx`
  come dataset `ccnl_registro`: 1.659 codici con status reale, tipo
  (dipendenti/AEC/parasubordinati), sottosezione, dirigenti e firmatari
  normalizzati.
- **Motivo**: l’API open data ha `stato = "acquisito"` su tutto e firmatari in
  testo libero; il foglio 1 dà status e flag per confederazione
  (Confindustria, Confapi, Confcommercio, Confesercenti, Confartigianato/CNA/Casa,
  Legacoop/Confcooperative/AGCI, CGIL/CISL/UIL, Confsal, Cisal, UGL).
- **Semantica dei flag**: “almeno una stesura firmata” (storico), non il testo
  corrente. La stringa `firmatari_*` è l’ultimo deposito; i due possono non
  coincidere (es. H011/C011/H05Y hanno UGL flag Sì ma il testo 2026 non elenca UGL).
- **AEC/parasubordinati**: 42 AEC + 19 parasubordinati nel registro; 58 codici
  hanno 0 dipendenti in Uniemens (agenti/collaboratori non sono dipendenti).
  Restano nel registro ma fuori dalle metriche teste.
- **Join**: `codice_ccnl` con metadata/applicazione; compose
  `mart_ccnl_intelligence` e `mart_ccnl_firmatari` aggiungono “chi firma” al
  peso 2024. Le quote per confederazione non sono una partizione (più firme
  sullo stesso codice).

## 2026-11-22 — Allineamento dati e universo

- **Anno di riferimento = ultimo anno con PA.** Il 2025 è pubblicato ma senza
  Conto Annuale: totali, quote e classifiche usano il 2024
  (`mart_ccnl_classifica`, `mart_ccnl_totali_anno`). Il 2025 resta disponibile
  per il solo privato, con `pa_inclusa = false`.
- **Genere = F / (F+M).** PA e lavoro domestico non hanno dettaglio di genere:
  la quota è `NULL`, non 0%. `genere_disponibile` esplicita la copertura.
- **Rinnovi su tutte le tipologie.** `mart_ccnl_rinnovi` prende l'ultimo accordo
  per codice (non solo "Testo definitivo") e la scadenza dell'ultimo accordo che
  la dichiara.
- **Classifiche omogenee.** `rank_nazionale` di `mart_ccnl_top` è dentro
  `ultimo_anno_con_dati` del singolo codice; per una classifica unica usare
  `mart_ccnl_classifica`.
- **H501 lavoro domestico**: serie che parte nel 2025; il salto datori 2024→2025
  è un cambio di perimetro, non crescita.
- **Territorio**: `CPUB` e `CDIV` sono aggregati non-CCNL; la geografia è
  pre-2016 (CI, OG, OT, VS) e include ESTERO. Non sommare territorio e nazionale.
- **PA 2025**: il Conto Annuale 2025 non è disponibile. Fino a pubblicazione,
  l'ultimo anno completo è il 2024.
- **Confluenze**: il file `principali-ccnl-storici.xlsx` ha cambiato header
  (`cod` → `id`) il 2026-11; l'extract riconosce entrambe le varianti.
- **Analisi Avanzata = mappa storica.** La classificazione CNEL si ferma al
  2023-06: 1.039 accordi successivi (630 codici, 14,8M dipendenti) non sono
  classificati. Non usare `ccnl_argomenti` per descrivere i rinnovi 2024–2026.
- **Nuovi codici 2025–2026.** 11 nuovi `id_ccnl` (catch-all, associazioni
  datoriali minori) non hanno metriche né confluenze. Monitorare l'ingresso
  nell'Excel applicazione prima di mapparli.

## 2026-10-10 — Corpus documentale fuori da main

- I testi CCNL (13 documenti, 8 estraibili) vivono sul branch
  `sperimentale/corpus-docs`, non in `main`.
- Il corpus è un progetto separato (`kind: corpus-project`), non un dataset
  toolkit: toolkit resta su anagrafica e metriche.
- OCR one-shot fuori CI; H011 (16,2% del privato) è una scansione.

## 2026-10-09 — Scope v0 tabellare

- v0 = anagrafica (API JSON) + metriche applicazione (Excel) + confluenze
  (Excel). Niente PDF/OCR in main.
- Territorio è un dataset dedicato (grana provincia × genere × anno).
- I mart sono analitici (ranking, quote, YoY, unnest ATECO), non passthrough.

## Fonti e licenza

- CNEL Archivio Contratti, Italian Open Data License v2.0.
- Dettaglio endpoint e file: [`sources.md`](sources.md).
