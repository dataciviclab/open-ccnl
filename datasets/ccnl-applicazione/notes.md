# Note — ccnl-applicazione

- Excel verificato 2026-10-09: ~1648 righe × 8 anni ≈ ~13k righe raw.
- Header multipli spazi (`n° datori di lavoro  2021`) → normalizzati in extract.
- Provinciali (fogli 2–4) in `ccnl-territorio`.
- **2025 senza PA**: i codici `S*` (Conto Annuale) sono a 0 nella fonte.
  `is_conto_annuale_ppaa` marca il blocco PA; usare il 2024 per i totali.
- **H501 lavoro domestico**: 0 fino al 2024, 523k nel 2025. Il salto datori
  2024→2025 è un cambio di perimetro, non crescita.
- **Genere**: F/M solo Uniemens (privato), dal 2023. PA e H501 non hanno
  genere: `genere_disponibile = false`, quota `NULL` (non 0).
