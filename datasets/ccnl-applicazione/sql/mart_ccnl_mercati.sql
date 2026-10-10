-- CNEL applicazione — MART analitico: mercati (sottosezione) per anno.
-- Legge solo da clean_input.

SELECT
    anno,
    nullif(trim(sottosezione), '') AS sottosezione,
    count(DISTINCT codice_ccnl) AS n_codici,
    count(DISTINCT codice_ccnl) FILTER (WHERE COALESCE(n_dipendenti, 0) > 0) AS n_codici_con_dipendenti,
    sum(COALESCE(n_dipendenti, 0)) AS n_dipendenti,
    sum(COALESCE(n_datori, 0)) AS n_datori,
    sum(COALESCE(n_dipendenti_f, 0)) AS n_dipendenti_f,
    sum(COALESCE(n_dipendenti_m, 0)) AS n_dipendenti_m,
    CASE
        WHEN sum(COALESCE(n_dipendenti, 0)) > 0
            THEN sum(COALESCE(n_dipendenti_f, 0))::DOUBLE / sum(COALESCE(n_dipendenti, 0))
    END AS quota_dipendenti_f
FROM clean_input
GROUP BY anno, nullif(trim(sottosezione), '')
HAVING sum(COALESCE(n_dipendenti, 0)) > 0 OR count(*) > 0
