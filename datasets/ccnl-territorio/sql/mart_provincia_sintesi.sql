-- CNEL territorio — MART: profilo delle province (tutti i CCNL sommati).
-- Legge solo da clean_input.

SELECT
    anno,
    sigla_provincia,
    any_value(provincia) AS provincia,
    any_value(regione) AS regione,
    sum(n_dipendenti) AS n_dipendenti,
    sum(n_dipendenti) FILTER (WHERE sesso = 'F') AS n_dipendenti_f,
    sum(n_dipendenti) FILTER (WHERE sesso = 'M') AS n_dipendenti_m,
    CASE
        WHEN sum(n_dipendenti) > 0
            THEN sum(n_dipendenti) FILTER (WHERE sesso = 'F')::DOUBLE
                 / sum(n_dipendenti)
    END AS quota_dipendenti_f,
    count(DISTINCT codice_ccnl) AS n_codici_ccnl,
    count(DISTINCT codice_ccnl) FILTER (WHERE n_dipendenti >= 1000) AS n_codici_rilevanti
FROM clean_input
GROUP BY anno, sigla_provincia
HAVING sum(n_dipendenti) > 0
