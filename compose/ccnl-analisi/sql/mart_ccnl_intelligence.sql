-- Compose intelligence — 1 riga per CCNL: peso + anagrafica + storia.
-- Support: applicazione (mart_ccnl_top), metadata (mart_ccnl_codici), confluenze (mart_ccnl_vigenti_confluenze).

WITH top AS (
    SELECT * FROM read_parquet('{support.applicazione.mart.mart_ccnl_top}')
),
codici AS (
    SELECT * FROM read_parquet('{support.metadata.mart.mart_ccnl_codici}')
),
storie AS (
    SELECT * FROM read_parquet('{support.confluenze.mart.mart_ccnl_vigenti_confluenze}')
),
ateco_agg AS (
    SELECT
        codice_ccnl,
        string_agg(DISTINCT settore_ateco, ';' ORDER BY settore_ateco) AS settori_ateco,
        count(DISTINCT settore_ateco) AS n_settori_ateco
    FROM read_parquet('{support.metadata.mart.mart_ccnl_ateco}')
    GROUP BY codice_ccnl
),
tot_2025 AS (
    SELECT sum(n_dipendenti) AS tot
    FROM top
    WHERE ultimo_anno_con_dati = 2025
)
SELECT
    t.codice_ccnl,
    t.ultimo_anno_con_dati,
    t.titolo,
    t.status,
    t.sottosezione,
    t.n_dipendenti,
    t.n_datori,
    t.n_dipendenti_f,
    t.n_dipendenti_m,
    t.quota_dipendenti_f,
    CASE
        WHEN t.ultimo_anno_con_dati = 2025 AND tt.tot > 0
            THEN t.n_dipendenti::DOUBLE / tt.tot
    END AS quota_dipendenti,
    t.rank_nazionale,
    t.anno_precedente,
    t.n_dipendenti_precedente,
    t.delta_dipendenti,
    t.delta_dipendenti_pct,
    c.n_stesure,
    c.n_testi_definitivi,
    c.n_rinnovi,
    c.n_accordi_economici,
    c.primo_deposito,
    c.ultimo_deposito,
    c.vita_anni_depositi,
    c.presente_in_corrente,
    c.settori_descrizione,
    a.settori_ateco,
    a.n_settori_ateco,
    COALESCE(s.n_codici_confluiti, 0) AS n_codici_confluiti,
    s.codici_confluiti,
    s.span_storico_anni,
    CASE
        WHEN t.n_dipendenti >= 1000000 THEN 'A_ge_1m'
        WHEN t.n_dipendenti >= 100000 THEN 'B_100k_1m'
        WHEN t.n_dipendenti >= 10000 THEN 'C_10k_100k'
        WHEN t.n_dipendenti >= 1000 THEN 'D_1k_10k'
        WHEN t.n_dipendenti > 0 THEN 'E_lt_1k'
        ELSE 'F_zero_o_assente'
    END AS fascia_peso
FROM top t
CROSS JOIN tot_2025 tt
LEFT JOIN codici c ON t.codice_ccnl = c.codice_ccnl
LEFT JOIN ateco_agg a ON t.codice_ccnl = a.codice_ccnl
LEFT JOIN storie s ON t.codice_ccnl = s.codice_vigente
