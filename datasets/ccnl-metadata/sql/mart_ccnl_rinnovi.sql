-- CNEL metadata — MART: radar rinnovi per codice.
--
-- Prende l'ultimo accordo dell'archivio corrente per ogni codice su TUTTE le
-- tipologie (non solo "Testo definitivo"): un "Accordo di rinnovo" più recente
-- può spostare la scadenza. La data_scadenza è quella dell'ultimo accordo che
-- la dichiara.
--
-- Determinismo: a parità di data/tipologia/pubblicazione il tiebreaker è
-- id_accordo DESC, così due run con lo stesso input danno lo stesso risultato.
-- Nota: scaduto e giorni_scaduto dipendono da current_date: il mart cambia
-- ogni giorno anche senza cambiare l'input.
-- Legge solo da clean_input.

WITH corrente AS (
    SELECT *
    FROM clean_input
    WHERE archivio = 'ARCHIVIO_CORRENTE'
),
ranked AS (
    SELECT
        *,
        row_number() OVER (
            PARTITION BY codice_ccnl
            ORDER BY
                data_stipula DESC NULLS LAST,
                CASE tipologia_accordo
                    WHEN 'Testo definitivo' THEN 0
                    WHEN 'Accordo di rinnovo' THEN 1
                    WHEN 'Economico secondo biennio' THEN 2
                    WHEN 'Accordo economico' THEN 3
                    WHEN 'Verbale Integrativo' THEN 4
                    ELSE 5
                END,
                data_pubblicazione DESC NULLS LAST,
                id_accordo DESC
        ) AS rn
    FROM corrente
),
ultimo AS (
    SELECT * FROM ranked WHERE rn = 1
),
scadenze AS (
    SELECT codice_ccnl, data_scadenza_contrattuale AS data_scadenza
    FROM (
        SELECT
            codice_ccnl,
            data_scadenza_contrattuale,
            row_number() OVER (
                PARTITION BY codice_ccnl
                ORDER BY data_stipula DESC NULLS LAST, id_accordo DESC
            ) AS rn
        FROM corrente
        WHERE data_scadenza_contrattuale IS NOT NULL
    )
    WHERE rn = 1
)
SELECT
    u.codice_ccnl,
    u.titolo_ccnl,
    u.tipologia_accordo AS tipologia_ultimo_accordo,
    u.data_stipula AS ultima_stipula,
    u.data_decorrenza AS decorrenza,
    s.data_scadenza,
    CASE
        WHEN s.data_scadenza < current_date
            THEN date_diff('day', s.data_scadenza, current_date)
    END AS giorni_scaduto,
    (s.data_scadenza < current_date) AS scaduto,
    u.ultimo_accordo_vigente,
    u.stato_aa
FROM ultimo u
LEFT JOIN scadenze s USING (codice_ccnl)
ORDER BY s.data_scadenza NULLS LAST, u.codice_ccnl
