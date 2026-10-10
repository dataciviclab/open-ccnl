-- CNEL applicazione — MART analitico: contratti "pesanti" e chi li guadagna/perde.
-- Ultimo anno con dati per ogni codice + confronto con l'anno precedente utile.
-- Legge solo da clean_input.

WITH with_data AS (
    SELECT
        codice_ccnl,
        anno,
        any_value(titolo) AS titolo,
        any_value(status) AS status,
        any_value(sottosezione) AS sottosezione,
        max(n_dipendenti) AS n_dipendenti,
        max(n_datori) AS n_datori,
        max(n_dipendenti_f) AS n_dipendenti_f,
        max(n_dipendenti_m) AS n_dipendenti_m
    FROM clean_input
    WHERE COALESCE(n_dipendenti, 0) > 0
    GROUP BY codice_ccnl, anno
),
latest AS (
    SELECT *
    FROM (
        SELECT
            *,
            row_number() OVER (
                PARTITION BY codice_ccnl
                ORDER BY anno DESC
            ) AS rn_latest
        FROM with_data
    ) WHERE rn_latest = 1
),
prev AS (
    SELECT *
    FROM (
        SELECT
            w.*,
            row_number() OVER (
                PARTITION BY w.codice_ccnl
                ORDER BY w.anno DESC
            ) AS rn_prev
        FROM with_data w
        JOIN latest l
          ON w.codice_ccnl = l.codice_ccnl
         AND w.anno < l.anno
    ) WHERE rn_prev = 1
)
SELECT
    l.codice_ccnl,
    l.anno AS ultimo_anno_con_dati,
    l.titolo,
    l.status,
    l.sottosezione,
    l.n_dipendenti,
    l.n_datori,
    l.n_dipendenti_f,
    l.n_dipendenti_m,
    CASE
        WHEN l.n_dipendenti_f IS NOT NULL
         AND l.n_dipendenti_m IS NOT NULL
         AND l.n_dipendenti > 0
            THEN l.n_dipendenti_f::DOUBLE / l.n_dipendenti
    END AS quota_dipendenti_f,
    p.anno AS anno_precedente,
    p.n_dipendenti AS n_dipendenti_precedente,
    l.n_dipendenti - p.n_dipendenti AS delta_dipendenti,
    CASE
        WHEN p.n_dipendenti IS NOT NULL
         AND p.n_dipendenti > 0
            THEN (l.n_dipendenti - p.n_dipendenti)::DOUBLE / p.n_dipendenti
    END AS delta_dipendenti_pct,
    rank() OVER (
        PARTITION BY l.anno
        ORDER BY l.n_dipendenti DESC, l.codice_ccnl
    ) AS rank_nazionale
FROM latest l
LEFT JOIN prev p ON l.codice_ccnl = p.codice_ccnl
