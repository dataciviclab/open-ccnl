-- Compose intelligence — top province per i principali CCNL (ultimo anno con dati).
-- Support: applicazione (top), territorio (mart_ccnl_provincia).

WITH top AS (
    SELECT codice_ccnl, titolo, n_dipendenti, rank_nazionale, ultimo_anno_con_dati
    FROM read_parquet('{support.applicazione.mart.mart_ccnl_top}')
    WHERE ultimo_anno_con_dati = 2025
      AND rank_nazionale <= 30
),
prov AS (
    SELECT * FROM read_parquet('{support.territorio.mart.mart_ccnl_provincia}')
    WHERE anno = 2025
),
ranked AS (
    SELECT
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
