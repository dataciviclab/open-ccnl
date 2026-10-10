# Decisions — open-ccnl

## 2026-10-09 — Scope v0

- **Decisione**: v0 = anagrafica (JSON API) + metriche applicazione (Excel) + confluenze (Excel). Niente PDF/OCR.
- **Motivo**: metriche già pronte e joinabili; corpus testuale eterogeneo (metà scansioni) — epica separata stile senato-akn.
- **Stato**: implementato in scaffold locale.

## 2026-10-09 — Location

- **Decisione**: scaffold in `esperimenti-locali/open-ccnl`, non `welfare-lavoro/`.
- **Motivo**: fuori funnel formale (mancano Discussion + source-check + issue intake).
- **Follow-up**: promozione solo dopo source-check `go intake`.

## 2026-10-09 — Excel = script non http_file

- **Decisione**: Excel multi-sheet scaricati via `extract.py` (`type: script`), non `http_file`.
- **Motivo**: toolkit non spacca multi-sheet; pattern open-inps / terzo-settore.

## 2026-10-09 — Mart analitici non passthrough

- **Decisione**: riscritti i mart in ranking, quote, YoY, unnest ATECO, indici di vita; aggiunto `compose/ccnl-analisi`.
- **Motivo**: un `GROUP BY` + `max()` di clean non è un mart. L’intelligence serve una riga per CCNL pronta all’analisi.
- **Compose**: support sui sibling; `{support.*.mart.*}` nei SQL; Makefile esegue `datasets/` prima di `compose/`.

## 2026-10-09 — Territorio come dataset dedicato

- **Decisione**: fogli provinciali → `datasets/ccnl-territorio` (non inside applicazione).
- **Motivo**: grana diversa (provincia × sesso × anno), volume ~4× nazionale, marts geo separati.
- **Incastro**: join `(codice_ccnl, anno)` con applicazione; compose aggiunge `mart_ccnl_geo` (top-5 province dei top-30 CCNL).

## 2026-10-09 — Corpus markdown (pattern italia-corpus)

- **Decisione**: testi definitivi top CCNL → `collezioni/**/*.md` con frontmatter + extract parquet.
- **Motivo**: PDF eterogenei (metà scansioni); il MD è greppabile, versionabile, usabile da agenti. Stesso pattern di `italia-corpus`.
- **Non è** un dataset toolkit primario: engine proprio (`kind: corpus-project` in `project.yml`); toolkit resta su anagrafica/metriche.
- ** qualità**: `qualita_testo` in frontmatter (text/scan/doc_binary). H011 #1 nazionale è scan → OCR come epica separata.

## 2026-10-10 — Gap analysis comparativa (L0+L1)

- **Decisione**: `lab_tools/istituti.py` (vocabolario 28 voci) + `analyze_istituti` → matrix + gap_score.
- **Motivo**: rispondere a “cosa va / non va” senza OCR e senza tabelle economiche. Segnale comparativo sul top text.
- **Pattern AI**: niente match su “algoritmi” grezzo (falsi positivi in metalmeccanica); solo contesto lavorativo.
- **Prossimo**: minimi via pdfplumber (L2) e/o OCR selettivo H011.

## 2026-10-10 — Chiusura chirurgica corpus (top-15)

- **Decisione**: scope corpus = `DEFAULT_CODES` (15 codici privati top per dipendenti), **frozen**. Coda top-30 scartata (<1% dipendenti ciascuno).
- **Fetch**: H442/J241 risultano scansioni (stesse di H011); B011 Word OLE2 → `doc_binary` (nessun converter di sistema); F012 escluso — CNEL deposita solo accordi di rinnovo, niente testo definitivo.
- **H052**: file `.rtf` è in realtà plain-text cp1252 → branch legacy in `fetch_cnel` (RTF vero o plain decodificato, guardia `_looks_like_text` contro binari) → ora `text` con 441 articoli.
- **Copertura raggiunta**: 8 testi = 34,6% dipendenti privati. H011 resta il buco (#1, 16,2%).

## 2026-10-10 — Contratto `qualita_testo: ocr` + OCR = artifact one-shot

- **Decisione**: nuovo valore frontmatter `ocr` (testo macchina RapidOCR, distinto da `text`). Gap analysis ammette `text` + `ocr` (`GAP_QUALITIES`); scan/doc_binary restano fuori.
- **OCR fuori CI**: 457 pagine H011 ≈ 40-60 min, dipendente da macchina — non è un job CI. Pattern italia-corpus: corpus MD = artifact committato; CI valida (test frontmatter/logica), non rigenera. OCR = one-shot locale al rinnovo del CCNL (~4 anni).
- **Strumento**: `--ocr` + `--ocr-workers` in `fetch_cnel`; `ocr_pdf` con worker paralleli (intra_op limitato). Testato su estratto H011 — qualità sufficiente per regex presence. Non eseguito sui top-5 scan in questa sessione (scelta tempo).
- **PA out of scope**: codici S* (comparto pubblico) = tipo documento diverso + caveat conto annuale — esclusi dal corpus con questa decisione.

## 2026-10-10 — Finding draft locale

- **Decisione**: bozza finding comparativo in `_local/notes/current/FINDING_ccnl_istituti_gap.md` (34,6% copertura, AI 1/8, I100 gap_score 0…). Pubblicazione Discussion solo su OK umano.
