-- CNEL confluenze — MART analitico: per ogni CCNL vigente, quante storie confluite e span storico.
-- Legge solo da clean_input (dopo la dedupa del mart edge list non è disponibile qui:
-- ricalcoliamo la priorità in CTE).

WITH edges AS (
    SELECT
        codice_confluito,
        codice_vigente,
        inizio_storia,
        fine_storia,
        sezione_ateco_desc,
        fonte,
        row_number() OVER (
            PARTITION BY codice_confluito
            ORDER BY
                CASE WHEN fonte = 'documento_riepilogativo' THEN 0 ELSE 1 END,
                fonte
        ) AS rn
    FROM clean_input
    WHERE nullif(trim(codice_vigente), '') IS NOT NULL
),
deduped AS (
    SELECT * FROM edges WHERE rn = 1
)
SELECT
    codice_vigente,
    count(*) AS n_codici_confluiti,
    string_agg(codice_confluito, ';' ORDER BY codice_confluito) AS codici_confluiti,
    min(inizio_storia) AS storia_da,
    max(fine_storia) AS storia_fino_a,
    max(date_diff('year', inizio_storia, coalesce(fine_storia, current_date))) AS span_storico_anni,
    count(DISTINCT nullif(sezione_ateco_desc, '')) AS n_sezioni_ateco
FROM deduped
GROUP BY codice_vigente
