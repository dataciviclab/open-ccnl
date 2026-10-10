-- Compose intelligence — 1 riga = CCNL × sezione ATECO, con peso.
-- Utile per join con appalti / imprese / territorio per ATECO.
-- Attenzione: il peso n_dipendenti è del CCNL intero (non ripartito per divisione).

WITH top AS (
    SELECT
        codice_ccnl,
        titolo,
        status,
        n_dipendenti,
        n_datori,
        rank_nazionale,
        quota_dipendenti_f
    FROM read_parquet('{support.applicazione.mart.mart_ccnl_top}')
),
ateco AS (
    SELECT * FROM read_parquet('{support.metadata.mart.mart_ccnl_ateco}')
)
SELECT
    t.codice_ccnl,
    a.settore_ateco,
    a.settori_descrizione AS sezione_ateco_desc,
    t.titolo,
    t.status,
    t.n_dipendenti,
    t.n_datori,
    t.rank_nazionale,
    t.quota_dipendenti_f,
    a.n_stesure,
    a.ultimo_deposito,
    a.presente_in_corrente
FROM top t
JOIN ateco a ON t.codice_ccnl = a.codice_ccnl
WHERE t.n_dipendenti IS NOT NULL
