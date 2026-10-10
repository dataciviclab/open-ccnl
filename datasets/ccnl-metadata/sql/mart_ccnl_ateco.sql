-- CNEL — MART analitico: un rigo per ATECO (sezione) × codice, per join territoriali/settoriali.
-- La colonna settori_ateco in clean è una stringa ";"; qui la si spezza in righe.
-- Legge solo da clean_input.

SELECT
    codice_ccnl,
    any_value(titolo_ccnl) AS titolo_ccnl,
    any_value(settori_descrizione) AS settori_descrizione,
    trim(ateco) AS settore_ateco,
    count(*) AS n_stesure,
    max(data_stipula) AS ultimo_deposito,
    bool_or(archivio = 'ARCHIVIO_CORRENTE') AS presente_in_corrente
FROM clean_input,
    unnest(string_split(settori_ateco, ';')) AS t(ateco)
WHERE nullif(trim(settori_ateco), '') IS NOT NULL
  AND nullif(trim(ateco), '') IS NOT NULL
GROUP BY codice_ccnl, trim(ateco)
