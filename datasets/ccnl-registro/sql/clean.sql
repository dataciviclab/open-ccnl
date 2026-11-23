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
    CASE WHEN nullif(trim(CAST(is_dirigenti AS VARCHAR)), '') IS NULL THEN NULL
         ELSE (lower(trim(CAST(is_dirigenti AS VARCHAR))) = 'true') END AS is_dirigenti,
    CASE WHEN nullif(trim(CAST(confindustria AS VARCHAR)), '') IS NULL THEN NULL
         ELSE (lower(trim(CAST(confindustria AS VARCHAR))) = 'true') END AS confindustria,
    CASE WHEN nullif(trim(CAST(confapi AS VARCHAR)), '') IS NULL THEN NULL
         ELSE (lower(trim(CAST(confapi AS VARCHAR))) = 'true') END AS confapi,
    CASE WHEN nullif(trim(CAST(confcommercio AS VARCHAR)), '') IS NULL THEN NULL
         ELSE (lower(trim(CAST(confcommercio AS VARCHAR))) = 'true') END AS confcommercio,
    CASE WHEN nullif(trim(CAST(confesercenti AS VARCHAR)), '') IS NULL THEN NULL
         ELSE (lower(trim(CAST(confesercenti AS VARCHAR))) = 'true') END AS confesercenti,
    CASE WHEN nullif(trim(CAST(confartigianato_cna_casa AS VARCHAR)), '') IS NULL THEN NULL
         ELSE (lower(trim(CAST(confartigianato_cna_casa AS VARCHAR))) = 'true') END AS confartigianato_cna_casa,
    CASE WHEN nullif(trim(CAST(legacoop_confcooperative_agci AS VARCHAR)), '') IS NULL THEN NULL
         ELSE (lower(trim(CAST(legacoop_confcooperative_agci AS VARCHAR))) = 'true') END AS legacoop_confcooperative_agci,
    CASE WHEN nullif(trim(CAST(cgil_cisl_uil AS VARCHAR)), '') IS NULL THEN NULL
         ELSE (lower(trim(CAST(cgil_cisl_uil AS VARCHAR))) = 'true') END AS cgil_cisl_uil,
    CASE WHEN nullif(trim(CAST(confsal AS VARCHAR)), '') IS NULL THEN NULL
         ELSE (lower(trim(CAST(confsal AS VARCHAR))) = 'true') END AS confsal,
    CASE WHEN nullif(trim(CAST(cisal AS VARCHAR)), '') IS NULL THEN NULL
         ELSE (lower(trim(CAST(cisal AS VARCHAR))) = 'true') END AS cisal,
    CASE WHEN nullif(trim(CAST(ugl AS VARCHAR)), '') IS NULL THEN NULL
         ELSE (lower(trim(CAST(ugl AS VARCHAR))) = 'true') END AS ugl
FROM raw_input
WHERE codice_ccnl IS NOT NULL
  AND codice_ccnl <> ''
