-- CNEL registro CCNL/AEC — CLEAN
-- Fonte: documento-riepilogativo-testi-depositati.xlsx, foglio "1 - tutti i codici".
-- Una riga per codice. Legge solo da raw_input.

SELECT
    upper(normalize_string(codice_ccnl)) AS codice_ccnl,
    normalize_string(sottosezione) AS sottosezione,
    lower(normalize_string(status)) AS status,
    lower(normalize_string(tipo_ccnl)) AS tipo_ccnl,
    normalize_string(titolo) AS titolo,
    normalize_string(firmatari_datoriali) AS firmatari_datoriali,
    normalize_string(firmatari_sindacali) AS firmatari_sindacali,
    normalize_string(firmatari_sindacali_tavolo_separato) AS firmatari_sindacali_tavolo_separato,
    normalize_string(firmatari_sindacali_adesione) AS firmatari_sindacali_adesione,
    (lower(trim(CAST(is_dirigenti AS VARCHAR))) = 'true') AS is_dirigenti,
    (lower(trim(CAST(confindustria AS VARCHAR))) = 'true') AS confindustria,
    (lower(trim(CAST(confapi AS VARCHAR))) = 'true') AS confapi,
    (lower(trim(CAST(confcommercio AS VARCHAR))) = 'true') AS confcommercio,
    (lower(trim(CAST(confesercenti AS VARCHAR))) = 'true') AS confesercenti,
    (lower(trim(CAST(confartigianato_cna_casa AS VARCHAR))) = 'true') AS confartigianato_cna_casa,
    (lower(trim(CAST(legacoop_confcooperative_agci AS VARCHAR))) = 'true') AS legacoop_confcooperative_agci,
    (lower(trim(CAST(cgil_cisl_uil AS VARCHAR))) = 'true') AS cgil_cisl_uil,
    (lower(trim(CAST(confsal AS VARCHAR))) = 'true') AS confsal,
    (lower(trim(CAST(cisal AS VARCHAR))) = 'true') AS cisal,
    (lower(trim(CAST(ugl AS VARCHAR))) = 'true') AS ugl
FROM raw_input
WHERE codice_ccnl IS NOT NULL
  AND codice_ccnl <> ''
