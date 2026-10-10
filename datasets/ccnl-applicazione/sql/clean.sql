-- CNEL applicazione CCNL — CLEAN
-- Numeri già arabi in fonte; normalizzo solo stringhe e null.

SELECT
    upper(normalize_string(codice_ccnl)) AS codice_ccnl,
    normalize_string(sottosezione) AS sottosezione,
    lower(normalize_string(status)) AS status,
    lower(normalize_string(tipo_ccnl)) AS tipo_ccnl,
    normalize_string(titolo) AS titolo,
    normalize_string(firmatari_datoriali) AS firmatari_datoriali,
    normalize_string(firmatari_sindacali) AS firmatari_sindacali,
    cast_int(anno) AS anno,
    cast_bigint(n_datori) AS n_datori,
    cast_bigint(n_dipendenti) AS n_dipendenti,
    cast_bigint(n_dipendenti_f) AS n_dipendenti_f,
    cast_bigint(n_dipendenti_m) AS n_dipendenti_m,
    normalize_string(filtri_conto_annuale_ppaa) AS filtri_conto_annuale_ppaa,
    normalize_string(fonte_note) AS fonte_note
FROM raw_input
WHERE codice_ccnl IS NOT NULL
  AND codice_ccnl <> ''
  AND cast_int(anno) IS NOT NULL;
