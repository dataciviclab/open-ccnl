-- CNEL registro — MART: una riga per codice, flag firmatari e classificazioni.
-- flag = almeno una stesura del codice firmata dalla confederazione (storico);
-- firmatari_* è la stringa dell'ultimo deposito e può non coincidere coi flag.
-- Cella vuota → NULL: se tutti i flag sono NULL la fascia è C_non_dichiarato.
-- Legge solo da clean_input.

SELECT
    codice_ccnl,
    status,
    tipo_ccnl,
    sottosezione,
    titolo,
    firmatari_datoriali,
    firmatari_sindacali,
    firmatari_sindacali_tavolo_separato,
    firmatari_sindacali_adesione,
    is_dirigenti,
    confindustria,
    confapi,
    confcommercio,
    confesercenti,
    confartigianato_cna_casa,
    legacoop_confcooperative_agci,
    cgil_cisl_uil,
    confsal,
    cisal,
    ugl,
    CASE
        WHEN nullif(trim(firmatari_datoriali), '') IS NULL THEN 0
        ELSE len(string_split(firmatari_datoriali, ';'))
    END AS n_firmatari_datoriali,
    CASE
        WHEN nullif(trim(firmatari_sindacali), '') IS NULL THEN 0
        ELSE len(string_split(firmatari_sindacali, ';'))
    END AS n_firmatari_sindacali,
    (
        (confindustria IS NOT NULL)::INT + (confapi IS NOT NULL)::INT
        + (confcommercio IS NOT NULL)::INT + (confesercenti IS NOT NULL)::INT
        + (confartigianato_cna_casa IS NOT NULL)::INT
        + (legacoop_confcooperative_agci IS NOT NULL)::INT
        + (cgil_cisl_uil IS NOT NULL)::INT + (confsal IS NOT NULL)::INT
        + (cisal IS NOT NULL)::INT + (ugl IS NOT NULL)::INT
    ) AS n_flag_dichiarati,
    (
        COALESCE(confindustria::INT, 0) + COALESCE(confapi::INT, 0)
        + COALESCE(confcommercio::INT, 0) + COALESCE(confesercenti::INT, 0)
        + COALESCE(confartigianato_cna_casa::INT, 0)
        + COALESCE(legacoop_confcooperative_agci::INT, 0)
        + COALESCE(cgil_cisl_uil::INT, 0) + COALESCE(confsal::INT, 0)
        + COALESCE(cisal::INT, 0) + COALESCE(ugl::INT, 0)
    ) AS n_flag_maggiori,
    COALESCE(
        confindustria OR confapi OR confcommercio OR confesercenti
        OR confartigianato_cna_casa OR legacoop_confcooperative_agci
        OR cgil_cisl_uil OR confsal OR cisal OR ugl,
        false
    ) AS ha_firmatari_maggiori,
    (
        confindustria IS NULL AND confapi IS NULL AND confcommercio IS NULL
        AND confesercenti IS NULL AND confartigianato_cna_casa IS NULL
        AND legacoop_confcooperative_agci IS NULL AND cgil_cisl_uil IS NULL
        AND confsal IS NULL AND cisal IS NULL AND ugl IS NULL
    ) AS tutti_flag_non_dichiarati,
    CASE
        WHEN (
            confindustria IS NULL AND confapi IS NULL AND confcommercio IS NULL
            AND confesercenti IS NULL AND confartigianato_cna_casa IS NULL
            AND legacoop_confcooperative_agci IS NULL AND cgil_cisl_uil IS NULL
            AND confsal IS NULL AND cisal IS NULL AND ugl IS NULL
        ) THEN 'C_non_dichiarato'
        WHEN COALESCE(
            confindustria OR confapi OR confcommercio OR confesercenti
            OR confartigianato_cna_casa OR legacoop_confcooperative_agci
            OR cgil_cisl_uil OR confsal OR cisal OR ugl,
            false
        ) THEN 'A_almeno_una_maggiore'
        ELSE 'B_solo_minori'
    END AS fascia_firmatari,
    (tipo_ccnl = 'accordo economico collettivo') AS is_aec,
    (tipo_ccnl = 'parasubordinati') AS is_parasubordinato,
    (sottosezione = 'CCNL di nuovo deposito') AS is_nuovo_deposito,
    (sottosezione = 'Settore pubblico') AS is_pubblico,
    (sottosezione = 'CCNL dirigenti settore privato') AS is_dirigenti_privato
FROM clean_input
