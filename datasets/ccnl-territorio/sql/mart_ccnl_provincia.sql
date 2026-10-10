-- CNEL territorio — MART: 1 riga = CCNL × anno × provincia (F+M sommati).
-- Legge solo da clean_input.

SELECT
    codice_ccnl,
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
    rank() OVER (
        PARTITION BY anno, sigla_provincia
        ORDER BY sum(n_dipendenti) DESC, codice_ccnl
    ) AS rank_nella_provincia
FROM clean_input
GROUP BY codice_ccnl, anno, sigla_provincia
HAVING sum(n_dipendenti) > 0
