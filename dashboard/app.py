#!/usr/bin/env python3
"""
Open CCNL · Dashboard
Archivio nazionale CCNL: peso, rinnovi e copertura argomenti.
"""

import streamlit as st
from lab_connectors.branding import apply_branding

st.set_page_config(
    page_title="Open CCNL · Dashboard",
    page_icon="📄",
    layout="wide",
    initial_sidebar_state="expanded",
)

apply_branding(
    repo_name="open-ccnl",
    repo_url="https://github.com/dataciviclab/open-ccnl",
)

pages = {
    "": [
        st.Page("pages/01_Panoramica.py", title="Panoramica", icon="📊", default=True),
        st.Page("pages/02_Applicazione.py", title="Applicazione", icon="👥"),
        st.Page("pages/03_Rinnovi.py", title="Rinnovi", icon="⏰"),
        st.Page("pages/04_Argomenti.py", title="Argomenti", icon="📑"),
        st.Page("pages/05_Territorio.py", title="Territorio", icon="🗺️"),
    ],
    "Strumenti": [
        st.Page("pages/06_SQL.py", title="Query SQL", icon="🧪"),
    ],
}

pg = st.navigation(pages, position="sidebar")

st.sidebar.markdown("---")
st.sidebar.caption("Fonte: CNEL open data · IODL v2.0")

pg.run()
