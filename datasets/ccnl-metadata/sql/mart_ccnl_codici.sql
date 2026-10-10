-- CNEL — MART analitico: anagrafica codici + profilo depositi + indici di vita.
-- Legge solo da clean_input.

SELECT
    codice_ccnl,
    any_value(titolo_ccnl) AS titolo_ccnl,
    any_value(settori_descrizione) AS settori_descrizione,
    any_value(settori_ateco) AS settori_ateco,
    any_value(settori_ateco_descrizione) AS settori_ateco_descrizione,
    count(*) AS n_stesure,
    count(*) FILTER (WHERE tipologia_accordo = 'Testo definitivo') AS n_testi_definitivi,
    count(*) FILTER (WHERE tipologia_accordo = 'Accordo di rinnovo') AS n_rinnovi,
    count(*) FILTER (WHERE tipologia_accordo = 'Accordo economico') AS n_accordi_economici,
    count(*) FILTER (WHERE tipologia_accordo = 'Verbale Integrativo') AS n_verbali,
    min(data_stipula) AS primo_deposito,
    max(data_stipula) AS ultimo_deposito,
    max(data_stipula) FILTER (WHERE ultimo_accordo_vigente) AS ultimo_stipula_vigente,
    date_diff('year', min(data_stipula), max(data_stipula)) AS vita_anni_depositi,
    count(DISTINCT EXTRACT(year FROM data_stipula)) AS n_anni_con_depositi,
    bool_or(archivio = 'ARCHIVIO_CORRENTE') AS presente_in_corrente,
    bool_or(ultimo_accordo_vigente) AS ha_stesura_vigente,
    any_value(parti_datoriali) AS parti_datoriali_sample,
    any_value(parti_sindacali) AS parti_sindacali_sample
FROM clean_input
GROUP BY codice_ccnl
