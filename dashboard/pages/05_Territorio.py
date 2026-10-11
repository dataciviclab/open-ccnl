"""Territorio — dove si concentrano i dipendenti coperti da CCNL."""

import pandas as pd
import plotly.express as px
import streamlit as st

from sources import TERRITORIO_ANNO, fmt_num, province, regioni

st.title("🗺️ Territorio")

reg = regioni()
prov = province()

if reg.empty:
    st.warning("Dati territoriali non disponibili.")
    st.stop()

reg_ult = reg[reg["anno"] == TERRITORIO_ANNO]
prov_ult = prov[prov["anno"] == TERRITORIO_ANNO]

k1, k2, k3, k4 = st.columns(4)
k1.metric("Regioni con dipendenti", fmt_num(reg_ult["regione"].nunique()))
k2.metric("Province con dipendenti", fmt_num(len(prov_ult)))
k3.metric("Dipendenti mappati", fmt_num(int(reg_ult["n_dipendenti"].sum())))
qf = reg_ult["n_dipendenti_f"].sum() / reg_ult["n_dipendenti"].sum()
k4.metric("Quota donne", f"{qf:.1%}")

col_a, col_b = st.columns(2)

with col_a:
    st.subheader("Dipendenti per regione")
    agg = (
        reg_ult.groupby("regione")
        .agg(n=("n_dipendenti", "sum"), f=("n_dipendenti_f", "sum"))
        .reset_index()
        .sort_values("n")
    )
    agg["quota_f"] = agg["f"] / agg["n"]
    fig = px.bar(
        agg,
        x="n",
        y="regione",
        orientation="h",
        custom_data=["quota_f"],
    )
    fig.update_layout(height=480, margin={"t": 10, "b": 30}, showlegend=False)
    fig.update_traces(
        marker_color="#6366f1",
        hovertemplate="%{y}<br>dipendenti: %{x:,.0f}<br>quote F: %{customdata[0]:.1%}<extra></extra>",
    )
    st.plotly_chart(fig, width="stretch")

with col_b:
    st.subheader("Le 15 province per dipendenti")
    top15 = prov_ult.nlargest(15, "n_dipendenti")
    fig = px.bar(
        top15.sort_values("n_dipendenti"),
        x="n_dipendenti",
        y="provincia",
        orientation="h",
        custom_data=["regione", "quota_dipendenti_f"],
    )
    fig.update_layout(height=480, margin={"t": 10, "b": 30}, showlegend=False)
    fig.update_traces(
        marker_color="#8b5cf6",
        hovertemplate="<b>%{y}</b> (%{customdata[0]})<br>dipendenti: %{x:,.0f}<br>quote F: %{customdata[1]:.1%}<extra></extra>",
    )
    st.plotly_chart(fig, width="stretch")

st.subheader("Regione × provincia — dove vive il totale")
fig = px.sunburst(
    prov_ult,
    path=["regione", "provincia"],
    values="n_dipendenti",
    color="quota_dipendenti_f",
    color_continuous_scale="RdBu",
    color_continuous_midpoint=0.5,
    hover_data={"quota_dipendenti_f": ":.1%"},
)
fig.update_layout(height=520, margin={"t": 10, "b": 30})
st.plotly_chart(fig, width="stretch")
st.caption("Colore = quota donne per provincia (blu ≈ parità, rosso ≈ maschile).")

st.subheader("Trend regionale")
tutte_reg = sorted(reg["regione"].unique())
default_reg = (
    reg[reg["anno"] == TERRITORIO_ANNO]
    .groupby("regione")["n_dipendenti"]
    .sum()
    .nlargest(8)
    .index.tolist()
)
sel = st.multiselect(
    "Regioni da confrontare",
    options=tutte_reg,
    default=default_reg,
)
if not sel:
    st.info("Seleziona almeno una regione.")
else:
    trend = (
        reg[reg["regione"].isin(sel)]
        .groupby(["anno", "regione"])["n_dipendenti"]
        .sum()
        .reset_index()
        .sort_values(["regione", "anno"])
    )
    fig = px.line(trend, x="anno", y="n_dipendenti", color="regione", markers=True)
    fig.update_layout(
        height=400,
        margin={"t": 10, "b": 30},
        yaxis_tickformat=",",
        xaxis=dict(dtick=1, tickmode="linear"),
    )
    st.plotly_chart(fig, width="stretch")

st.caption(
    f"Fonte: dipendenti Uniemens per provincia × genere ({TERRITORIO_ANNO - 2}–{TERRITORIO_ANNO}). "
    "PA con conto annuale può essere sotto-rappresentata."
)
