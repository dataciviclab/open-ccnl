-- CNEL Analisi Avanzata — CLEAN accordi × sotto-argomento
-- Legge solo da raw_input.

SELECT
    cast_bigint(id_accordo) AS id_accordo,
    upper(normalize_string(codice_ccnl)) AS codice_ccnl,
    upper(normalize_string(codice_argomento)) AS codice_argomento,
    normalize_string(nome_argomento) AS nome_argomento,
    upper(normalize_string(codice_macro)) AS codice_macro,
    normalize_string(nome_macro) AS nome_macro,
    normalize_string(tipologia_accordo) AS tipologia_accordo,
    TRY_CAST(data_stipula AS DATE) AS data_stipula,
    TRY_CAST(data_decorrenza AS DATE) AS data_decorrenza,
    TRY_CAST(data_scadenza_contrattuale AS DATE) AS data_scadenza_contrattuale,
    normalize_string(titolo_ccnl) AS titolo_ccnl,
    normalize_string(settori_ateco) AS settori_ateco,
    normalize_string(stato_aa) AS stato_aa,
    (ultimo_accordo_vigente = 'true') AS ultimo_accordo_vigente
FROM raw_input
WHERE id_accordo IS NOT NULL
  AND codice_argomento IS NOT NULL
  AND codice_argomento <> ''
