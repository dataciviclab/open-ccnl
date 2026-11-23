-- CNEL registro — MART: una riga per codice, flag firmatari e classificazioni.
-- flag = almeno una stesura del codice firmata dalla confederazione (storico);
-- firmatari_* è la stringa dell'ultimo deposito e può non coincidere coi flag.
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
        confindustria::INT + confapi::INT + confcommercio::INT + confesercenti::INT
        + confartigianato_cna_casa::INT + legacoop_confcooperative_agci::INT
        + cgil_cisl_uil::INT + confsal::INT + cisal::INT + ugl::INT
    ) AS n_flag_maggiori,
    (
        confindustria OR confapi OR confcommercio OR confesercenti
        OR confartigianato_cna_casa OR legacoop_confcooperative_agci
        OR cgil_cisl_uil OR confsal OR cisal OR ugl
    ) AS ha_firmatari_maggiori,
    CASE
        WHEN (
            confindustria OR confapi OR confcommercio OR confesercenti
            OR confartigianato_cna_casa OR legacoop_confcooperative_agci
            OR cgil_cisl_uil OR confsal OR cisal OR ugl
        ) THEN 'A_almeno_una_maggiore'
        ELSE 'B_solo_minori'
    END AS fascia_firmatari,
    (tipo_ccnl = 'accordo economico collettivo') AS is_aec,
    (tipo_ccnl = 'parasubordinati') AS is_parasubordinato,
    (sottosezione = 'CCNL di nuovo deposito') AS is_nuovo_deposito,
    (sottosezione = 'Settore pubblico') AS is_pubblico,
    (sottosezione = 'CCNL dirigenti settore privato') AS is_dirigenti_privato
FROM clean_input
