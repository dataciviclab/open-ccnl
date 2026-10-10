-- CNEL confluenze — CLEAN
-- Legge solo da raw_input.

SELECT
    normalize_string(fonte) AS fonte,
    upper(normalize_string(codice_confluito)) AS codice_confluito,
    normalize_string(confluenze_intermedie) AS confluenze_intermedie,
    upper(normalize_string(codice_vigente)) AS codice_vigente,
    normalize_string(titolo_confluito) AS titolo_confluito,
    normalize_string(titolo_vigente) AS titolo_vigente,
    upper(normalize_string(sezione_ateco)) AS sezione_ateco,
    normalize_string(sezione_ateco_desc) AS sezione_ateco_desc,
    TRY_CAST(inizio_storia AS DATE) AS inizio_storia,
    TRY_CAST(fine_storia AS DATE) AS fine_storia
FROM raw_input
WHERE codice_confluito IS NOT NULL
  AND codice_confluito <> ''
  AND codice_vigente IS NOT NULL
  AND codice_vigente <> '';
