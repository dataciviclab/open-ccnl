-- Compose intelligence — top province per i principali CCNL.
-- Usa la classifica omogenea sull'ultimo anno con PA (mart_ccnl_classifica)
-- e lo stesso anno per il territorio. La PA non ha dettaglio provinciale in
-- questa fonte: i CCNL del conto annuale non compaiono nel join.
-- Support: applicazione (classifica), territorio (mart_ccnl_provincia).

WITH rif AS (
    SELECT max(anno_riferimento) AS anno
    FROM read_parquet('{support.applicazione.mart.mart_ccnl_classifica}')
),
top AS (
    SELECT c.*
    FROM read_parquet('{support.applicazione.mart.mart_ccnl_classifica}') c, rif
    WHERE c.anno_riferimento = rif.anno
      AND c.rank_nazionale <= 30
),
prov AS (
    SELECT p.*
    FROM read_parquet('{support.territorio.mart.mart_ccnl_provincia}') p, rif
    WHERE p.anno = rif.anno
),
ranked AS (
    SELECT
        t.anno_riferimento,
        t.codice_ccnl,
        t.titolo,
        t.n_dipendenti AS n_dipendenti_nazionali,
        t.rank_nazionale,
        p.sigla_provincia,
        p.provincia,
        p.regione,
        p.n_dipendenti AS n_dipendenti_provincia,
        p.quota_dipendenti_f,
        p.rank_nella_provincia,
        row_number() OVER (
            PARTITION BY t.codice_ccnl
            ORDER BY p.n_dipendenti DESC, p.sigla_provincia
        ) AS rank_geo
    FROM top t
    JOIN prov p ON t.codice_ccnl = p.codice_ccnl
)
SELECT
    anno_riferimento,
    codice_ccnl,
    titolo,
    n_dipendenti_nazionali,
    rank_nazionale,
    rank_geo,
    sigla_provincia,
    provincia,
    regione,
    n_dipendenti_provincia,
    CASE
        WHEN n_dipendenti_nazionali > 0
            THEN n_dipendenti_provincia::DOUBLE / n_dipendenti_nazionali
    END AS quota_sul_nazionale,
    quota_dipendenti_f
FROM ranked
WHERE rank_geo <= 5
