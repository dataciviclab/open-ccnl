"""Argomenti — cosa coprono i CCNL secondo la classificazione ufficiale CNEL."""

import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st

from sources import argomenti_stats, codici_pivot, intelligence

st.title("📑 Copertura argomenti (Analisi Avanzata CNEL)")

stats = argomenti_stats()
pivot = codici_pivot()
df = intelligence()

st.caption(
    "Classificazione ufficiale CNEL su 4.812 accordi (tutte le stesure). "
    "Presenza dell'argomento, non testo della clausola."
)

k1, k2, k3 = st.columns(3)
k1.metric("Argomenti classificati", f"{len(stats)} sotto-argomenti")
k2.metric("Accordi × argomento", f"{int(stats['n_accordi'].sum()):,}".replace(",", "."))
k3.metric("Codici CCNL coperti", f"{int(pivot['codice_ccnl'].nunique())}")

col_a, col_b = st.columns(2)

with col_a:
    st.subheader("I 15 argomenti più classificati")
    top = stats.nlargest(15, "n_accordi")
    fig = px.bar(
        top.sort_values("n_accordi"),
        x="n_accordi",
        y="nome_argomento",
        orientation="h",
        custom_data=["codice_argomento", "n_codici_ccnl"],
    )
    fig.update_layout(height=480, margin={"t": 10, "b": 30}, showlegend=False)
    fig.update_traces(
        hovertemplate="<b>%{customdata[0]}</b> %{y}<br>accordi: %{x:,.0f}<br>codici CCNL: %{customdata[1]}<extra></extra>"
    )
    st.plotly_chart(fig, width="stretch")

with col_b:
    st.subheader("Quanti argomenti copre ogni CCNL")
    dist = pivot["n_argomenti"].value_counts().sort_index()
    fig = px.bar(
        x=dist.index,
        y=dist.values,
        labels={"x": "n. argomenti coperti", "y": "n. codici CCNL"},
    )
    fig.update_layout(height=480, margin={"t": 10, "b": 30}, showlegend=False)
    fig.update_traces(marker_color="#8b5cf6", hovertemplate="argomenti: %{x}<br>codici: %{y}<extra></extra>")
    st.plotly_chart(fig, width="stretch")

st.subheader("Heatmap: top 12 CCNL per dipendenti × argomenti chiave")
KEY = ["TE1", "CR5", "CR6", "TE3", "OR6", "RS8", "SR1", "OR1"]
LABELS = {
    "TE1": "minimi",
    "CR5": "TFR",
    "CR6": "prev. integr.",
    "TE3": "scatti",
    "OR6": "ferie",
    "RS8": "bilaterali",
    "SR1": "malattia",
    "OR1": "orario",
}
with_dip = df[df["n_dipendenti"].fillna(0) > 0].nlargest(12, "n_dipendenti")
p = pivot[pivot["codice_ccnl"].isin(with_dip["codice_ccnl"])][["codice_ccnl"] + KEY]
m = (
    with_dip[["codice_ccnl", "titolo"]]
    .merge(p, on="codice_ccnl")
    .set_index("codice_ccnl")
)
m["label"] = m.index + " — " + m["titolo"].str.slice(0, 32)
matrix = m[KEY].astype(int)
fig = px.imshow(
    matrix,
    x=[LABELS.get(c, c) for c in KEY],
    y=m["label"].tolist(),
    color_continuous_scale=[[0, "#0e1117"], [1, "#6366f1"]],
    aspect="auto",
)
fig.update_layout(height=440, margin={"t": 10, "b": 30}, coloraxis_showscale=False)
st.plotly_chart(fig, width="stretch")

st.subheader("I 15 CCNL per dipendenti × indicatori")
top15 = with_dip[
    ["codice_ccnl", "titolo", "n_dipendenti", "n_argomenti_aa", "aa_minimi", "aa_tfr", "aa_scatti", "aa_ferie", "aa_bilaterali"]
].copy()
top15 = top15.rename(
    columns={
        "n_argomenti_aa": "n_argomenti",
        "aa_minimi": "minimi",
        "aa_tfr": "TFR",
        "aa_scatti": "scatti",
        "aa_ferie": "ferie",
        "aa_bilaterali": "bilaterali",
    }
)
top15["n_dipendenti"] = top15["n_dipendenti"].map(lambda v: f"{int(v):,}".replace(",", "."))
top15["titolo"] = top15["titolo"].str.slice(0, 45)
st.dataframe(top15, width="stretch", hide_index=True)

st.caption(
    "Il CCNL più applicato (H011 Terziario) risulta classificato su 66 argomenti "
    "anche se il suo PDF depositato è una scansione: la copertura AA non dipende dal text layer."
)
