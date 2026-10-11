"""Panoramica — il sistema contrattuale italiano in una schermata."""

import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st

from sources import fmt_num, intelligence, mercati, rinnovi

st.title("📊 Panoramica del sistema contrattuale")

df = intelligence()
ren = rinnovi()
mk = mercati()

if df.empty:
    st.warning("Nessun dato disponibile.")
    st.stop()

with_dip = df[df["n_dipendenti"].fillna(0) > 0].copy()
tot_dip = with_dip["n_dipendenti"].sum()
top5 = with_dip.nlargest(5, "n_dipendenti")["n_dipendenti"].sum()

ren = ren.merge(df[["codice_ccnl", "n_dipendenti"]], on="codice_ccnl", how="left")
oggi = pd.Timestamp.today().normalize()
scaduti = ren[pd.to_datetime(ren["data_scadenza"], errors="coerce") < oggi]
dip_scaduti = scaduti["n_dipendenti"].fillna(0).sum()

# ── KPI ─────────────────────────────────────────────────────────────
k1, k2, k3, k4, k5 = st.columns(5)
k1.metric("CCNL con peso", fmt_num(len(with_dip)))
k2.metric("Dipendenti coperti", fmt_num(int(tot_dip)))
k3.metric(
    "Top-5 concentrazione",
    f"{100 * top5 / tot_dip:.0f}%",
    help="Quota di dipendenti coperta dai 5 CCNL più grandi",
)
k4.metric(
    "Dip. sotto scaduti",
    fmt_num(int(dip_scaduti)),
    delta=f"{100 * dip_scaduti / tot_dip:.0f}% del totale",
    delta_color="inverse",
)
k5.metric(
    "Copertura testi AA",
    f"{int((df['n_argomenti_aa'] > 0).sum())} codici",
    help="CCNL con almeno un argomento classificato in Analisi Avanzata",
)

st.divider()

# ── Composizione: peso + scadenze ───────────────────────────────────
col_a, col_b = st.columns(2)

with col_a:
    st.subheader("Dipendenti per fascia di peso")
    fascia = (
        with_dip.groupby("fascia_peso")["n_dipendenti"]
        .sum()
        .reset_index()
        .sort_values("fascia_peso")
    )
    labels = {
        "A_ge_1m": "≥ 1M",
        "B_100k_1m": "100k–1M",
        "C_10k_100k": "10k–100k",
        "D_1k_10k": "1k–10k",
        "E_lt_1k": "< 1k",
        "F_zero_o_assente": "0/assente",
    }
    fascia["fascia"] = fascia["fascia_peso"].map(labels).fillna(fascia["fascia_peso"])
    fig = px.bar(
        fascia,
        x="fascia",
        y="n_dipendenti",
        custom_data=["n_dipendenti"],
    )
    fig.update_layout(height=320, margin={"t": 10, "b": 30}, showlegend=False)
    fig.update_traces(marker_color="#6366f1", hovertemplate="%{y:,.0f}<extra></extra>")
    st.plotly_chart(fig, width="stretch")

with col_b:
    st.subheader("Scadenze: vigenti vs scaduti")
    n_vig = len(ren) - len(scaduti)
    fig = go.Figure(
        go.Pie(
            labels=["Scaduti (rinnovo dovuto)", "Con scadenza futura"],
            values=[len(scaduti), n_vig],
            hole=0.55,
            marker_colors=["#f59e0b", "#6366f1"],
        )
    )
    fig.update_layout(height=320, margin={"t": 10, "b": 30}, showlegend=True)
    st.plotly_chart(fig, width="stretch")

st.subheader("I 15 CCNL per numero di dipendenti")
top15 = with_dip.nlargest(15, "n_dipendenti")[
    ["codice_ccnl", "titolo", "n_dipendenti", "n_argomenti_aa"]
].copy()
top15["titolo"] = top15["titolo"].str.slice(0, 60)
fig = px.bar(
    top15.sort_values("n_dipendenti"),
    x="n_dipendenti",
    y="titolo",
    orientation="h",
    custom_data=["codice_ccnl", "n_argomenti_aa"],
)
fig.update_layout(height=480, margin={"t": 10, "b": 30}, showlegend=False)
fig.update_traces(
    hovertemplate="<b>%{customdata[0]}</b><br>dipendenti: %{x:,.0f}<br>argomenti AA: %{customdata[1]}<extra></extra>"
)
st.plotly_chart(fig, width="stretch")

st.subheader("Mercati (sottosezione) per dipendenti — ultimo anno")
mk_ult = mk[mk["anno"] == mk["anno"].max()].nlargest(8, "n_dipendenti")
mk_ult = mk_ult[mk_ult["n_dipendenti"] > 0]
fig = px.bar(
    mk_ult.sort_values("n_dipendenti"),
    x="n_dipendenti",
    y="sottosezione",
    orientation="h",
)
fig.update_layout(height=340, margin={"t": 10, "b": 30}, showlegend=False)
fig.update_traces(marker_color="#8b5cf6", hovertemplate="%{y}<br>%{x:,.0f}<extra></extra>")
st.plotly_chart(fig, width="stretch")

st.caption("Dati: CNEL open data (Uniemens + Analisi Avanzata) · IODL v2.0")
