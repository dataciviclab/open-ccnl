-- CNEL territorio — CLEAN
-- Legge solo da raw_input. Grana: codice × anno × provincia × sesso.

SELECT
    cast_int(anno) AS anno,
    upper(normalize_string(codice_ccnl)) AS codice_ccnl,
    normalize_string(regione) AS regione,
    upper(normalize_string(sigla_provincia)) AS sigla_provincia,
    normalize_string(provincia) AS provincia,
    upper(normalize_string(sesso)) AS sesso,
    cast_bigint(n_dipendenti) AS n_dipendenti
FROM raw_input
WHERE codice_ccnl IS NOT NULL
  AND codice_ccnl <> ''
  AND cast_int(anno) IS NOT NULL
  AND nullif(upper(trim(sigla_provincia)), '') IS NOT NULL
  AND upper(trim(sesso)) IN ('F', 'M');
