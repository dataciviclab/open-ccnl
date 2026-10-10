-- Copertura per sotto-argomento: quanti accordi e quanti codici CCNL
SELECT
    codice_argomento,
    argmax(nome_argomento, codice_argomento) AS nome_argomento,
    argmax(codice_macro, codice_argomento) AS codice_macro,
    argmax(nome_macro, codice_argomento) AS nome_macro,
    count(*) AS n_accordi,
    count(DISTINCT codice_ccnl) AS n_codici_ccnl,
    count(*) FILTER (WHERE tipologia_accordo = 'Testo definitivo') AS n_testi_definitivi,
    min(data_stipula) AS prima_stipula,
    max(data_stipula) AS ultima_stipula
FROM clean_input
GROUP BY codice_argomento
ORDER BY n_accordi DESC
