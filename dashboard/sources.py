"""Fonti dati per la dashboard Open CCNL.

Wrappa lab_connectors.duckdb.queries con @st.cache_data.
Risoluzione: GCS (dati sincronizzati dalla pipeline) o out/data/ locale
(auto-detect).
"""

from __future__ import annotations

from pathlib import Path

import streamlit as st

from lab_connectors.duckdb.queries import (
    detect_local_root,
    load_mart_table as _load_mart_table,
    query_clean as _query_clean,
)

ROOT = Path(__file__).parent.parent
PREFIX = "open-ccnl/"
YEAR = 2026
LOCAL_ROOT = detect_local_root(repo_root=ROOT)

SLUG_APPLICAZIONE = "ccnl_applicazione"
SLUG_METADATA = "ccnl_metadata"
SLUG_TERRITORIO = "ccnl_territorio"
SLUG_ARGOMENTI = "ccnl_argomenti"
SLUG_ANALISI = "ccnl_analisi"

TERRITORIO_ANNO = 2025


@st.cache_data(ttl=3600, show_spinner=False)
def load_mart(slug: str, table: str, year: int = YEAR):
    """Carica un singolo mart table (cached 1h)."""
    return _load_mart_table(slug, table, year, prefix=PREFIX, local_root=LOCAL_ROOT)


@st.cache_data(ttl=3600, show_spinner=False)
def query_clean(slug: str, sql: str, year: int = YEAR):
    """Esegue SQL sul clean layer di uno slug (cached 1h)."""
    return _query_clean(slug, sql, [year], prefix=PREFIX, local_root=LOCAL_ROOT)


# ── Views di comodo sulle pagine ────────────────────────────────────

@st.cache_data(ttl=3600, show_spinner=False)
def intelligence():
    """Mart intelligence: 1 riga per CCNL con peso, storia e argomenti."""
    return load_mart(SLUG_ANALISI, "mart_ccnl_intelligence")


@st.cache_data(ttl=3600, show_spinner=False)
def argomenti_stats():
    return load_mart(SLUG_ARGOMENTI, "mart_argomenti_stats")


@st.cache_data(ttl=3600, show_spinner=False)
def codici_pivot():
    return load_mart(SLUG_ARGOMENTI, "mart_codici_pivot")


@st.cache_data(ttl=3600, show_spinner=False)
def mercati():
    return load_mart(SLUG_APPLICAZIONE, "mart_ccnl_mercati")


@st.cache_data(ttl=3600, show_spinner=False)
def regioni():
    """Mart regione (run 2026, colonna anno = 2023–2025). Filtro anno in pagina."""
    return load_mart(SLUG_TERRITORIO, "mart_ccnl_regione")


@st.cache_data(ttl=3600, show_spinner=False)
def province():
    """Mart provincia sintesi (run 2026, colonna anno = 2023–2025)."""
    return load_mart(SLUG_TERRITORIO, "mart_provincia_sintesi")


@st.cache_data(ttl=3600, show_spinner=False)
def rinnovi():
    """Ultimo testo definitivo per codice con scadenza + peso Uniemens.

    Nota: niente CTE top-level — query_clean wrappa con un suo WITH.
    """
    sql = """
    SELECT
        codice_ccnl,
        data_stipula AS ultima_stipula,
        data_scadenza_contrattuale AS data_scadenza,
        titolo_ccnl
    FROM clean_input
    WHERE tipologia_accordo = 'Testo definitivo'
      AND archivio = 'ARCHIVIO_CORRENTE'
      AND codice_ccnl IS NOT NULL
    QUALIFY row_number() OVER (
        PARTITION BY codice_ccnl
        ORDER BY data_stipula DESC NULLS LAST
    ) = 1
    """
    return query_clean(SLUG_METADATA, sql)


from lab_connectors.formatters import fmt_eur, fmt_num, fmt_pct  # noqa: E402

__all__ = [
    "intelligence",
    "argomenti_stats",
    "codici_pivot",
    "rinnovi",
    "mercati",
    "regioni",
    "province",
    "query_clean",
    "load_mart",
    "SLUG_METADATA",
    "SLUG_APPLICAZIONE",
    "TERRITORIO_ANNO",
    "fmt_eur",
    "fmt_num",
    "fmt_pct",
]
