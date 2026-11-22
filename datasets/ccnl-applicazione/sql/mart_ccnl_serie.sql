-- CNEL applicazione — MART analitico: serie lunga con quote, rank e variazioni.
-- Legge solo da clean_input.
--
-- Semantica dei missing:
-- - la PA è coperta dal Conto Annuale (is_conto_annuale_ppaa = true) e non ha
--   il dettaglio F/M in Uniemens: quota_dipendenti_f è NULL, non 0.
-- - pa_inclusa = false segnala un anno in cui il blocco PA non ha dati
--   (es. 2025): i totali e le quote di quell'anno non sono confrontabili
--   con gli anni precedenti.

WITH base AS (
    SELECT
        codice_ccnl,
        anno,
        any_value(titolo) AS titolo,
        any_value(status) AS status,
        any_value(tipo_ccnl) AS tipo_ccnl,
        any_value(sottosezione) AS sottosezione,
        bool_or(is_conto_annuale_ppaa) AS is_conto_annuale_ppaa,
        max(n_datori) AS n_datori,
        max(n_dipendenti) AS n_dipendenti,
        max(n_dipendenti_f) AS n_dipendenti_f,
        max(n_dipendenti_m) AS n_dipendenti_m,
        any_value(filtri_conto_annuale_ppaa) AS filtri_conto_annuale_ppaa
    FROM clean_input
    GROUP BY codice_ccnl, anno
),
totals AS (
    SELECT
        anno,
        sum(n_dipendenti) AS totale_dipendenti_anno,
        sum(n_datori) AS totale_datori_anno,
        count(*) FILTER (WHERE COALESCE(n_dipendenti, 0) > 0) AS n_ccnl_con_dipendenti,
        count(*) FILTER (WHERE is_conto_annuale_ppaa AND COALESCE(n_dipendenti, 0) > 0) AS n_ccnl_pa_con_dipendenti
    FROM base
    GROUP BY anno
),
enriched AS (
    SELECT
        b.*,
        t.totale_dipendenti_anno,
        t.totale_datori_anno,
        t.n_ccnl_con_dipendenti,
        t.n_ccnl_pa_con_dipendenti,
        (t.n_ccnl_pa_con_dipendenti > 0) AS pa_inclusa,
        CASE
            WHEN t.totale_dipendenti_anno > 0 AND b.n_dipendenti IS NOT NULL
                THEN b.n_dipendenti::DOUBLE / t.totale_dipendenti_anno
        END AS quota_dipendenti_anno,
        (COALESCE(b.n_dipendenti_f, 0) + COALESCE(b.n_dipendenti_m, 0) > 0) AS genere_disponibile,
        CASE
            WHEN COALESCE(b.n_dipendenti_f, 0) + COALESCE(b.n_dipendenti_m, 0) > 0
                THEN b.n_dipendenti_f::DOUBLE
                     / (b.n_dipendenti_f + b.n_dipendenti_m)
        END AS quota_dipendenti_f,
        rank() OVER (
            PARTITION BY b.anno
            ORDER BY COALESCE(b.n_dipendenti, -1) DESC, b.codice_ccnl
        ) AS rank_dipendenti_anno,
        lag(b.n_dipendenti) OVER (
            PARTITION BY b.codice_ccnl ORDER BY b.anno
        ) AS n_dipendenti_anno_prec,
        lag(b.n_datori) OVER (
            PARTITION BY b.codice_ccnl ORDER BY b.anno
        ) AS n_datori_anno_prec
    FROM base b
    JOIN totals t USING (anno)
)
SELECT
    codice_ccnl,
    anno,
    titolo,
    status,
    tipo_ccnl,
    sottosezione,
    is_conto_annuale_ppaa,
    n_datori,
    n_dipendenti,
    n_dipendenti_f,
    n_dipendenti_m,
    genere_disponibile,
    quota_dipendenti_f,
    filtri_conto_annuale_ppaa,
    totale_dipendenti_anno,
    totale_datori_anno,
    n_ccnl_con_dipendenti,
    n_ccnl_pa_con_dipendenti,
    pa_inclusa,
    quota_dipendenti_anno,
    rank_dipendenti_anno,
    n_dipendenti_anno_prec,
    n_datori_anno_prec,
    n_dipendenti - n_dipendenti_anno_prec AS delta_dipendenti,
    CASE
        WHEN n_dipendenti_anno_prec IS NOT NULL
         AND n_dipendenti_anno_prec > 0
         AND n_dipendenti IS NOT NULL
            THEN (n_dipendenti - n_dipendenti_anno_prec)::DOUBLE / n_dipendenti_anno_prec
    END AS delta_dipendenti_pct
FROM enriched
