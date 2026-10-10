# open-ccnl

Archivio nazionale dei **Contratti Collettivi Nazionali di Lavoro** (CNEL) —
anagrafica, metriche di applicazione (Uniemens/INPS) e grafo confluenze.

> Repo **sperimentale locale** (`esperimenti-locali/`). Non è ancora un repo
> Lab ufficiale: niente publish automatico, niente registry org.
>
> La sperimentazione sul **corpus documentale** (testi MD dei CCNL, gap
> analysis istituti, OCR) vive su branch locale `sperimentale/corpus-docs`.

## Fonte

| Componente | URL | Formato |
|---|---|---|
| API open data metadata | `az-apim-cne-sa-0002-lgc-we.azure-api.net/.../open-data` | JSON |
| Dati applicazione CCNL | CNEL Excel “dati-sull'applicazione-dei-ccnl-dal-2018” | XLSX multi-sheet |
| Confluenze / storici | CNEL Excel documento-riepilogativo + principali-storici | XLSX |

Licenza fonte: Italian Open Data License v2.0 (CNEL).

## Dataset (v0)

| Slug | Contenuto | Grano |
|---|---|---|
| `ccnl-metadata` | Codici, tipologie, date, firmatari, ATECO | 1 riga = 1 accordo depositato |
| `ccnl-applicazione` | Datori, dipendenti, F/M per anno 2018–2025 | 1 riga = CCNL × anno |
| `ccnl-territorio` | Dipendenti per provincia × genere (2023–2025) | 1 riga = CCNL × prov × sesso × anno |
| `ccnl-confluenze` | Mappa confluenze storiche dei codici | 1 riga = codice confluito |

### Mart analitici

| Dataset | Mart | Uso |
|---|---|---|
| applicazione | `mart_ccnl_serie` | serie lunga: quota, rank/anno, YoY |
| applicazione | `mart_ccnl_top` | ranking nazionale ultimo anno + delta |
| applicazione | `mart_ccnl_mercati` | aggregate per sottosezione × anno (F/M) |
| metadata | `mart_ccnl_codici` | profilo depositi per codice (stesure, vita) |
| metadata | `mart_ccnl_ateco` | 1 riga = codice × sezione ATECO |
| territorio | `mart_ccnl_provincia` | CCNL × provincia × anno (F/M, rank locale) |
| territorio | `mart_ccnl_regione` | CCNL × regione + n. provincie |
| territorio | `mart_provincia_sintesi` | profilo provincia (tutti i CCNL) |
| confluenze | `mart_ccnl_confluenze` | edge list grafo confluenze |
| confluenze | `mart_ccnl_vigenti_confluenze` | n. storie per vigente |
| **compose/ccnl-analisi** | **`mart_ccnl_intelligence`** | **peso × anagrafica × ATECO × storia** |
| compose/ccnl-analisi | `mart_ccnl_settori` | codice × ATECO con peso |
| compose/ccnl-analisi | `mart_ccnl_geo` | top-5 province per top-30 CCNL |

**Fuori v0 del layer metriche**: OCR sistematico, estrazione minimi retributivi.

## Quickstart

```bash
# dipendenze pipeline (nel venv del workspace)
uv pip install -e ".[pipeline,dev]" --system

make check   # preflight config
make run     # scarica + clean + mart (export TOOLKIT_ALLOW_SCRIPT_SOURCE=1 già nel Makefile)
```

Output: `out/data/{raw,clean,mart}/<slug>/<year>/`.

## Note di merito dati

- Il campo `dipendenti` nell'API JSON è quasi sempre `null`: le metriche stanno
  nell'Excel applicazione (fonte INPS Uniemens + conto annuale PPAA per la PA).
- Alcuni CCNL PA hanno dipendenti Uniemens = 0: il dato è sul conto annuale
  (colonna `filtri su conto annuale PPAA`).
- Lavoro domestico (H501) appare con un flusso Uniemens diverso dal 2025.
- 2025 può essere parziale (media 12 mesi a chiusura estrazione).
- F012 (edili): il CNEL deposita solo accordi di rinnovo, niente testo definitivo.

## Stato

- [ ] source-check formale SO (`cnel.it`)
- [ ] Discussion Domanda (ancora pubblica)
- [ ] Promozione fuori da `esperimenti-locali/`
- [x] Layer tabellare v0 completo (4 dataset + 12 mart + compose)
- [ ] Dashboard consultazione (valutare, layer tabellare)
- Corpus documentale: branch `sperimentale/corpus-docs` (frozen, v. decisions.md)
