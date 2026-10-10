-- Edge list: codice CCNL × sotto-argomento con numero di stesure classificate
SELECT
    codice_ccnl,
    codice_argomento,
    argmax(nome_argomento, (codice_ccnl, codice_argomento)) AS nome_argomento,
    argmax(nome_macro, (codice_ccnl, codice_argomento)) AS nome_macro,
    count(*) AS n_stesure,
    count(*) FILTER (WHERE tipologia_accordo = 'Testo definitivo') AS n_testi_definitivi,
    max(data_stipula) AS ultima_stipula
FROM clean_input
WHERE codice_ccnl <> ''
GROUP BY codice_ccnl, codice_argomento
ORDER BY codice_ccnl, codice_argomento
