-- CNEL registro — MART: copertura per confederazione firmataria.
-- flag = almeno una stesura del codice firmata dalla confederazione (storico),
-- NON necessariamente il testo/ultimo deposito corrente.
-- Un codice può avere più firmatari: le somme per confederazione non sono una
-- partizione e possono superare il totale dei codici.
-- Legge solo da clean_input.

WITH long AS (
    SELECT codice_ccnl, status, tipo_ccnl, sottosezione,
           'confindustria' AS confederazione, 'datoriale' AS tipo, confindustria AS flag
    FROM clean_input
    UNION ALL
    SELECT codice_ccnl, status, tipo_ccnl, sottosezione,
           'confapi', 'datoriale', confapi
    FROM clean_input
    UNION ALL
    SELECT codice_ccnl, status, tipo_ccnl, sottosezione,
           'confcommercio', 'datoriale', confcommercio
    FROM clean_input
    UNION ALL
    SELECT codice_ccnl, status, tipo_ccnl, sottosezione,
           'confesercenti', 'datoriale', confesercenti
    FROM clean_input
    UNION ALL
    SELECT codice_ccnl, status, tipo_ccnl, sottosezione,
           'confartigianato_cna_casa', 'datoriale', confartigianato_cna_casa
    FROM clean_input
    UNION ALL
    SELECT codice_ccnl, status, tipo_ccnl, sottosezione,
           'legacoop_confcooperative_agci', 'datoriale', legacoop_confcooperative_agci
    FROM clean_input
    UNION ALL
    SELECT codice_ccnl, status, tipo_ccnl, sottosezione,
           'cgil_cisl_uil', 'sindacale', cgil_cisl_uil
    FROM clean_input
    UNION ALL
    SELECT codice_ccnl, status, tipo_ccnl, sottosezione,
           'confsal', 'sindacale', confsal
    FROM clean_input
    UNION ALL
    SELECT codice_ccnl, status, tipo_ccnl, sottosezione,
           'cisal', 'sindacale', cisal
    FROM clean_input
    UNION ALL
    SELECT codice_ccnl, status, tipo_ccnl, sottosezione,
           'ugl', 'sindacale', ugl
    FROM clean_input
),
tot AS (
    SELECT count(*) AS totale FROM clean_input
)
SELECT
    confederazione,
    tipo,
    count(*) FILTER (WHERE flag) AS n_codici_con_flag,
    round(
        100.0 * count(*) FILTER (WHERE flag) / max(tot.totale),
        1
    ) AS pct_codici_con_flag,
    count(*) FILTER (WHERE flag AND status = 'vigente') AS n_vigenti,
    count(*) FILTER (WHERE flag AND tipo_ccnl = 'dipendenti') AS n_dipendenti,
    count(*) FILTER (WHERE flag AND tipo_ccnl = 'accordo economico collettivo') AS n_aec,
    count(*) FILTER (WHERE flag AND tipo_ccnl = 'parasubordinati') AS n_parasubordinati,
    count(*) FILTER (WHERE flag AND sottosezione = 'Settore pubblico') AS n_pubblico,
    count(*) FILTER (WHERE flag AND sottosezione = 'CCNL di nuovo deposito') AS n_nuovo_deposito
FROM long
CROSS JOIN tot
GROUP BY confederazione, tipo
ORDER BY n_codici_con_flag DESC, confederazione
