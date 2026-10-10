-- CNEL territorio — MART: 1 riga = CCNL × anno × regione.
-- Legge solo da clean_input.

SELECT
    codice_ccnl,
    anno,
    regione,
    sum(n_dipendenti) AS n_dipendenti,
    sum(n_dipendenti) FILTER (WHERE sesso = 'F') AS n_dipendenti_f,
    sum(n_dipendenti) FILTER (WHERE sesso = 'M') AS n_dipendenti_m,
    count(DISTINCT sigla_provincia) FILTER (WHERE n_dipendenti > 0) AS n_provincie_con_dipendenti,
    CASE
        WHEN sum(n_dipendenti) > 0
            THEN sum(n_dipendenti) FILTER (WHERE sesso = 'F')::DOUBLE
                 / sum(n_dipendenti)
    END AS quota_dipendenti_f
FROM clean_input
GROUP BY codice_ccnl, anno, regione
HAVING sum(n_dipendenti) > 0
