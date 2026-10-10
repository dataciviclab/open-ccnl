-- CNEL archivio CCNL — CLEAN anagrafica
-- Legge solo da raw_input. Date ISO già in fonte; nulla di italiano da normalizzare.

SELECT
    normalize_string(archivio) AS archivio,
    cast_bigint(id_accordo) AS id_accordo,
    cast_bigint(id_ccnl) AS id_ccnl,
    upper(normalize_string(codice_ccnl)) AS codice_ccnl,
    normalize_string(identificativo_accordo) AS identificativo_accordo,
    normalize_string(ambito) AS ambito,
    normalize_string(tipologia_accordo) AS tipologia_accordo,
    normalize_string(titolo) AS titolo,
    normalize_string(titolo_ccnl) AS titolo_ccnl,
    lower(normalize_string(stato)) AS stato,
    normalize_string(stato_aa) AS stato_aa,
    TRY_CAST(data_stipula AS DATE) AS data_stipula,
    TRY_CAST(data_decorrenza AS DATE) AS data_decorrenza,
    TRY_CAST(data_scadenza_contrattuale AS DATE) AS data_scadenza_contrattuale,
    TRY_CAST(data_scadenza_economica AS DATE) AS data_scadenza_economica,
    TRY_CAST(data_pubblicazione AS DATE) AS data_pubblicazione,
    (ultimo_accordo_vigente = 'true') AS ultimo_accordo_vigente,
    (visibile_online = 'true') AS visibile_online,
    parti_datoriali,
    parti_sindacali,
    settori,
    settori_descrizione,
    settori_ateco,
    settori_ateco_descrizione,
    sottosettori_descrizione
FROM raw_input
WHERE id_accordo IS NOT NULL
  AND codice_ccnl IS NOT NULL
  AND codice_ccnl <> '';
