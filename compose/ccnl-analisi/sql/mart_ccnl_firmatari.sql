-- Compose — peso dei contratti per confederazione firmataria.
-- Usa la classifica 2024 (peso omogeneo) e i flag del registro CNEL.
-- flag = almeno una stesura del codice firmata dalla confederazione (storico),
-- NON necessariamente il testo corrente.
-- ATTENZIONE: un CCNL può avere più firmatari; le quote per confederazione
-- non sono una partizione e la loro somma può superare il 100%.
-- Support: applicazione (mart_ccnl_classifica), registro (mart_ccnl_registro).

WITH classifica AS (
    SELECT codice_ccnl, n_dipendenti AS n_dipendenti_riferimento
    FROM read_parquet('{support.applicazione.mart.mart_ccnl_classifica}')
),
registro AS (
    SELECT * FROM read_parquet('{support.registro.mart.mart_ccnl_registro}')
),
long AS (
    SELECT codice_ccnl, 'confindustria' AS confederazione, 'datoriale' AS tipo, confindustria AS flag
    FROM registro
    UNION ALL
    SELECT codice_ccnl, 'confapi', 'datoriale', confapi FROM registro
    UNION ALL
    SELECT codice_ccnl, 'confcommercio', 'datoriale', confcommercio FROM registro
    UNION ALL
    SELECT codice_ccnl, 'confesercenti', 'datoriale', confesercenti FROM registro
    UNION ALL
    SELECT codice_ccnl, 'confartigianato_cna_casa', 'datoriale', confartigianato_cna_casa FROM registro
    UNION ALL
    SELECT codice_ccnl, 'legacoop_confcooperative_agci', 'datoriale', legacoop_confcooperative_agci FROM registro
    UNION ALL
    SELECT codice_ccnl, 'cgil_cisl_uil', 'sindacale', cgil_cisl_uil FROM registro
    UNION ALL
    SELECT codice_ccnl, 'confsal', 'sindacale', confsal FROM registro
    UNION ALL
    SELECT codice_ccnl, 'cisal', 'sindacale', cisal FROM registro
    UNION ALL
    SELECT codice_ccnl, 'ugl', 'sindacale', ugl FROM registro
),
tot AS (
    SELECT sum(n_dipendenti_riferimento) AS totale FROM classifica
)
SELECT
    l.confederazione,
    l.tipo,
    count(*) FILTER (WHERE l.flag) AS n_codici,
    count(*) FILTER (WHERE l.flag AND c.n_dipendenti_riferimento > 0) AS n_codici_con_peso,
    sum(c.n_dipendenti_riferimento) FILTER (WHERE l.flag) AS n_dipendenti_riferimento,
    round(
        100.0 * sum(c.n_dipendenti_riferimento) FILTER (WHERE l.flag)
        / max(tot.totale),
        1
    ) AS quota_su_totale_pct
FROM long l
LEFT JOIN classifica c USING (codice_ccnl)
CROSS JOIN tot
GROUP BY l.confederazione, l.tipo
ORDER BY n_dipendenti_riferimento DESC, l.confederazione
