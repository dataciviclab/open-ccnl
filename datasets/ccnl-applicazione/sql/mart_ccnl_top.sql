-- CNEL applicazione — MART analitico: ultimo dato disponibile per codice.
--
-- ATTENZIONE: una riga per codice, con l'ultimo anno in cui il codice ha
-- dipendenti. Anni diversi convivono nello stesso mart (es. PA ferma al 2024
-- e privato al 2025): per classifiche omogenee usare mart_ccnl_classifica.
-- rank_nazionale è calcolato DENTRO ultimo_anno_con_dati, non sul totale.
--
-- quota_dipendenti_f = F / (F+M), NULL quando F e M sono entrambi assenti
-- (PA/conto annuale e lavoro domestico): 0% è un dato reale, non un missing.
-- Legge solo da clean_input.

WITH with_data AS (
    SELECT
        codice_ccnl,
        anno,
        any_value(titolo) AS titolo,
        any_value(status) AS status,
        any_value(sottosezione) AS sottosezione,
        bool_or(is_conto_annuale_ppaa) AS is_conto_annuale_ppaa,
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
    l.anno AS anno_riferimento,
    l.titolo,
    l.status,
    l.sottosezione,
    l.is_conto_annuale_ppaa,
    l.n_dipendenti,
    l.n_datori,
    l.n_dipendenti_f,
    l.n_dipendenti_m,
    (COALESCE(l.n_dipendenti_f, 0) + COALESCE(l.n_dipendenti_m, 0) > 0) AS genere_disponibile,
    CASE
        WHEN COALESCE(l.n_dipendenti_f, 0) + COALESCE(l.n_dipendenti_m, 0) > 0
            THEN l.n_dipendenti_f::DOUBLE
                 / (l.n_dipendenti_f + l.n_dipendenti_m)
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
