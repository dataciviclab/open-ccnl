"""Query SQL — Interroga direttamente i dati."""

from pathlib import Path

from lab_connectors.duckdb.sql_page import render_sql_query
from lab_connectors.registry import load_registry

registry = load_registry(
    Path(__file__).parent.parent.parent / "registry" / "registry.json"
)

render_sql_query(
    registry=registry,
    years=[2026],  # anni di RUN dei parquet (≠ time_coverage dei dati)
    prefix="open-ccnl/",
    default_slug="ccnl_applicazione",
    title="🧪 Query SQL",
    description=(
        "Interroga i dataset del repo. Usa ``clean_input`` come nome della "
        "tabella virtuale — viene risolta automaticamente sul dataset selezionato."
    ),
)
