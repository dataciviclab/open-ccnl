"""Rinnovi — quali contratti scaduti pesano di più, e da quanto."""

import pandas as pd
import plotly.express as px
import streamlit as st

from sources import fmt_num, intelligence, rinnovi

st.title("⏰ Radar dei rinnovi contrattuali")

ren = rinnovi()
df = intelligence()[["codice_ccnl", "n_dipendenti", "rank_nazionale", "fascia_peso"]]
tab = ren.merge(df, on="codice_ccnl", how="left")
tab["n_dipendenti"] = tab["n_dipendenti"].fillna(0).astype(int)
tab["data_scadenza"] = pd.to_datetime(tab["data_scadenza"], errors="coerce")

oggi = pd.Timestamp.today().normalize()
scaduti = tab[tab["data_scadenza"] < oggi].copy()
scaduti["giorni_scaduto"] = (oggi - scaduti["data_scadenza"]).dt.days
scaduti = scaduti.sort_values("n_dipendenti", ascending=False)

k1, k2, k3, k4 = st.columns(4)
k1.metric("Ultimi testi definitivi", fmt_num(len(tab)))
k2.metric("…con scadenza nota", fmt_num(int(tab["data_scadenza"].notna().sum())))
k3.metric("Di cui scaduti", fmt_num(len(scaduti)))
k4.metric(
    "Dipendenti sotto scaduti",
    fmt_num(int(scaduti["n_dipendenti"].sum())),
    delta="rinnovo teoricamente dovuto",
    delta_color="inverse",
)

st.divider()

col_a, col_b = st.columns(2)

with col_a:
    st.subheader("Giorni di ritardo vs peso (top 30)")
    top30 = scaduti.head(30)
    fig = px.scatter(
        top30,
        x="giorni_scaduto",
        y="n_dipendenti",
        hover_name="codice_ccnl",
        hover_data=["titolo_ccnl"],
        log_y=True,
    )
    fig.update_layout(
        height=380,
        margin={"t": 10, "b": 30},
        yaxis=dict(
            tickvals=[10_000, 50_000, 100_000, 500_000, 1_000_000, 2_500_000],
            ticktext=["10k", "50k", "100k", "500k", "1M", "2,5M"],
        ),
    )
    fig.update_traces(marker_color="#f59e0b", marker_size=10)
    st.plotly_chart(fig, width="stretch")
    st.caption("Asse Y logaritmica — un contratto scaduto da 3 anni con 2,5M dipendenti pesa.")

with col_b:
    st.subheader("Scaduti per fascia di peso")
    fascia = (
        scaduti.groupby("fascia_peso")
        .agg(n_ccnl=("codice_ccnl", "count"), n_dip=("n_dipendenti", "sum"))
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
        fascia.sort_values("n_dip", ascending=True),
        x="n_dip",
        y="fascia",
        orientation="h",
        custom_data=["n_ccnl"],
    )
    fig.update_layout(height=380, margin={"t": 10, "b": 30}, showlegend=False)
    fig.update_traces(
        marker_color="#ef4444",
        hovertemplate="%{y}<br>dipendenti: %{x:,.0f}<br>ccnl: %{customdata[0]}<extra></extra>",
    )
    st.plotly_chart(fig, width="stretch")

st.subheader("Scaduti, per peso Uniemens")
show = scaduti.head(30)[
    [
        "codice_ccnl",
        "titolo_ccnl",
        "ultima_stipula",
        "data_scadenza",
        "giorni_scaduto",
        "n_dipendenti",
    ]
].rename(
    columns={
        "codice_ccnl": "codice",
        "titolo_ccnl": "titolo",
        "ultima_stipula": "stipula",
        "data_scadenza": "scadenza",
        "giorni_scaduto": "giorni da scadenza",
        "n_dipendenti": "dipendenti",
    }
)
st.dataframe(show, width="stretch", hide_index=True)

with st.expander("Tutti i CCNL con scadenza nota"):
    st.dataframe(
        tab.dropna(subset=["data_scadenza"]).sort_values("data_scadenza")[
            ["codice_ccnl", "titolo_ccnl", "ultima_stipula", "data_scadenza", "n_dipendenti"]
        ],
        width="stretch",
        hide_index=True,
    )

st.caption(
    "Scadenza = ultimo testo definitivo vigente con data nota. "
    "Un rinnovo può essere firmato senza nuovo testo depositato: usa come segnale, non come verità giuridica."
)
