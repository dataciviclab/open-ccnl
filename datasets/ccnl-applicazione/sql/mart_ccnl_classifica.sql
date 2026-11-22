-- CNEL applicazione — MART: classifica omogenea sull'ultimo anno con PA.
--
-- L'anno di riferimento è il più recente in cui la PA ha dati (Conto Annuale).
-- Esclude gli anni "senza PA" (es. 2025) per non mescolare universi diversi.
-- Una riga per codice con dipendenti > 0, rank calcolato sullo stesso anno.
-- Legge solo da clean_input.

WITH base AS (
    SELECT
        codice_ccnl,
        anno,
        any_value(titolo) AS titolo,
        any_value(status) AS status,
        any_value(sottosezione) AS sottosezione,
        bool_or(is_conto_annuale_ppaa) AS is_conto_annuale_ppaa,
        max(n_datori) AS n_datori,
        max(n_dipendenti) AS n_dipendenti,
        max(n_dipendenti_f) AS n_dipendenti_f,
        max(n_dipendenti_m) AS n_dipendenti_m
    FROM clean_input
    GROUP BY codice_ccnl, anno
),
anni AS (
    SELECT
        anno,
        count(*) FILTER (WHERE is_conto_annuale_ppaa AND COALESCE(n_dipendenti, 0) > 0) AS n_pa,
        sum(n_dipendenti) AS totale_dipendenti_anno
    FROM base
    GROUP BY anno
),
rif AS (
    SELECT max(anno) AS anno
    FROM anni
    WHERE n_pa > 0
)
SELECT
    b.codice_ccnl,
    b.anno AS anno_riferimento,
    b.titolo,
    b.status,
    b.sottosezione,
    b.is_conto_annuale_ppaa,
    b.n_datori,
    b.n_dipendenti,
    b.n_dipendenti_f,
    b.n_dipendenti_m,
    (COALESCE(b.n_dipendenti_f, 0) + COALESCE(b.n_dipendenti_m, 0) > 0) AS genere_disponibile,
    CASE
        WHEN COALESCE(b.n_dipendenti_f, 0) + COALESCE(b.n_dipendenti_m, 0) > 0
            THEN b.n_dipendenti_f::DOUBLE
                 / (b.n_dipendenti_f + b.n_dipendenti_m)
    END AS quota_dipendenti_f,
    a.totale_dipendenti_anno,
    CASE
        WHEN a.totale_dipendenti_anno > 0 AND b.n_dipendenti IS NOT NULL
            THEN b.n_dipendenti::DOUBLE / a.totale_dipendenti_anno
    END AS quota_dipendenti_anno,
    rank() OVER (
        ORDER BY COALESCE(b.n_dipendenti, -1) DESC, b.codice_ccnl
    ) AS rank_nazionale,
    CASE
        WHEN b.n_dipendenti >= 1000000 THEN 'A_ge_1m'
        WHEN b.n_dipendenti >= 100000 THEN 'B_100k_1m'
        WHEN b.n_dipendenti >= 10000 THEN 'C_10k_100k'
        WHEN b.n_dipendenti >= 1000 THEN 'D_1k_10k'
        WHEN b.n_dipendenti > 0 THEN 'E_lt_1k'
        ELSE 'F_zero_o_assente'
    END AS fascia_peso
FROM base b
JOIN anni a USING (anno)
CROSS JOIN rif r
WHERE b.anno = r.anno
  AND COALESCE(b.n_dipendenti, 0) > 0
