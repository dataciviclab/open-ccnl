-- CNEL applicazione — MART: totali onesti per anno.
-- pa_inclusa = false segnala un anno senza il blocco PA (Conto Annuale non
-- disponibile, es. 2025): totale e quote non sono confrontabili con gli anni
-- precedenti. quota_donne_fm_pct usa F+M (universo con genere); l'altra usa
-- il totale e quindi sottostima quando la PA è inclusa.
-- Legge solo da clean_input.

SELECT
    anno,
    count(DISTINCT codice_ccnl) AS n_codici,
    count(*) FILTER (WHERE COALESCE(n_dipendenti, 0) > 0) AS n_codici_con_dipendenti,
    count(*) FILTER (WHERE is_conto_annuale_ppaa AND COALESCE(n_dipendenti, 0) > 0) AS n_codici_pa_con_dipendenti,
    sum(n_dipendenti) AS n_dipendenti,
    sum(n_datori) AS n_datori,
    sum(n_dipendenti_f) AS n_dipendenti_f,
    sum(n_dipendenti_m) AS n_dipendenti_m,
    round(
        100.0 * sum(n_dipendenti_f)
        / nullif(sum(n_dipendenti_f) + sum(n_dipendenti_m), 0),
        1
    ) AS quota_donne_fm_pct,
    round(
        100.0 * sum(n_dipendenti_f) / nullif(sum(n_dipendenti), 0),
        1
    ) AS quota_donne_totale_pct,
    (count(*) FILTER (WHERE is_conto_annuale_ppaa AND COALESCE(n_dipendenti, 0) > 0) > 0) AS pa_inclusa
FROM clean_input
GROUP BY anno
ORDER BY anno
