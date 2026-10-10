-- Matrice presenza: 1 riga = codice CCNL, colonne = 88 sotto-argomenti (0/1)
-- + n_argomenti = quanti sotto-argomenti distinti copre il codice
WITH pivoted AS (
    PIVOT clean_input
    ON codice_argomento
    USING count(*) > 0
    GROUP BY codice_ccnl
),
counts AS (
    SELECT
        codice_ccnl,
        count(DISTINCT codice_argomento) AS n_argomenti
    FROM clean_input
    WHERE codice_ccnl <> ''
    GROUP BY codice_ccnl
)
SELECT p.*, c.n_argomenti
FROM pivoted p
JOIN counts c USING (codice_ccnl)
