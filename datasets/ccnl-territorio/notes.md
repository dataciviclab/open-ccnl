# Note — ccnl-territorio

- Verificato 2026-10-09: 2023=54.614 righe, 2024=55.623, 2025=56.270.
- Somma provinciale 2025 ≈ 15,69M vs nazionale 2025 15,66M: coincidenza, non
  stesso universo.
- Header: 2023 usa `CODICE_CCNL`, 2024-25 `CODICE_CONTRATTO`.
- Join con applicazione: `(codice_ccnl, anno)`.
- **Aggregati non-CCNL**: `CPUB` (~475k) e `CDIV` (~155k) non esistono in
  `ccnl_applicazione`; non sono contratti, non vanno sommati ai CCNL.
- **PA**: il territorio non ha il dettaglio PA (Conto Annuale) e non ha H501.
- **Geografia**: 108 sigle includono ESTERO e 4 province sarde soppresse nel
  2016 (`CI`, `OG`, `OT`, `VS`). Mappare prima di join con ISTAT.
