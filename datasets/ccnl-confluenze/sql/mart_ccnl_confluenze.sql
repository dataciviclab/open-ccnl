-- CNEL confluenze — MART: edge list del grafo (codice confluito → vigente).
-- 1 riga per codice confluito (priorità a documento_riepilogativo).
-- Legge solo da clean_input.

WITH ranked AS (
    SELECT
        *,
        row_number() OVER (
            PARTITION BY codice_confluito
            ORDER BY
                CASE WHEN fonte = 'documento_riepilogativo' THEN 0 ELSE 1 END,
                fonte
        ) AS rn
    FROM clean_input
)
SELECT
    codice_confluito,
    codice_vigente,
    confluenze_intermedie,
    titolo_confluito,
    titolo_vigente,
    sezione_ateco,
    sezione_ateco_desc,
    inizio_storia,
    fine_storia,
    fonte AS fonte_prioritaria
FROM ranked
WHERE rn = 1
