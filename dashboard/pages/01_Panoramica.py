"""Panoramica — il sistema contrattuale italiano in una schermata."""

import plotly.express as px
import plotly.graph_objects as go
import streamlit as st
from sources import classifica, fmt_num, intelligence, mercati, rinnovi, totali_anno

st.title("📊 Panoramica del sistema contrattuale")

intel = intelligence()
ren = rinnovi()
mk = mercati()
tot = totali_anno()

if intel.empty or tot.empty:
    st.warning("Nessun dato disponibile.")
    st.stop()

# Ultimo anno in cui la PA ha dati: unica base corretta per totali e classifiche.
rif = tot[tot["pa_inclusa"]].sort_values("anno").iloc[-1]
anno_rif = int(rif["anno"])
tot_dip = int(rif["n_dipendenti"])

cl = classifica()
with_dip = cl[cl["n_dipendenti"].fillna(0) > 0].copy()
top5 = with_dip.nlargest(5, "n_dipendenti")["n_dipendenti"].sum()

ren = ren.merge(cl[["codice_ccnl", "n_dipendenti"]], on="codice_ccnl", how="left")
scaduti = ren[ren["scaduto"] == True]  # noqa: E712
dip_scaduti = scaduti["n_dipendenti"].fillna(0).sum()

# ── KPI ─────────────────────────────────────────────────────────────
k1, k2, k3, k4, k5 = st.columns(5)
k1.metric("CCNL con peso", fmt_num(len(with_dip)))
k2.metric("Dipendenti coperti", fmt_num(tot_dip), help=f"Anno di riferimento {anno_rif} (PA inclusa)")
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
    "Copertura argomenti AA",
    f"{int((intel['n_argomenti_aa'] > 0).sum())} codici",
    help="CCNL con almeno un argomento classificato in Analisi Avanzata",
)

st.caption(
    f"Totali e classifiche sull'anno {anno_rif}: è l'ultimo con la PA (Conto Annuale). "
    "Il 2025 è pubblicato ma senza PA: non è confrontabile sul totale."
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
    scad = ren["scaduto"].fillna(False).astype(bool)
    ha_scadenza = ren["data_scadenza"].notna()
    n_scaduti = int(scad.sum())
    n_futuri = int((~scad & ha_scadenza).sum())
    n_senza = int((~ha_scadenza).sum())
    fig = go.Figure(
        go.Pie(
            labels=["Scaduti (rinnovo dovuto)", "Scadenza futura", "Senza scadenza"],
            values=[n_scaduti, n_futuri, n_senza],
            hole=0.55,
            marker_colors=["#f59e0b", "#6366f1", "#94a3b8"],
        )
    )
    fig.update_layout(height=320, margin={"t": 10, "b": 30}, showlegend=True)
    st.plotly_chart(fig, width="stretch")

st.subheader("I 15 CCNL per numero di dipendenti")
top15 = (
    with_dip.nlargest(15, "n_dipendenti")[["codice_ccnl", "titolo", "n_dipendenti"]]
    .merge(intel[["codice_ccnl", "n_argomenti_aa"]], on="codice_ccnl", how="left")
)
top15["n_argomenti_aa"] = top15["n_argomenti_aa"].fillna(0).astype(int)
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

st.subheader(f"Mercati (sottosezione) per dipendenti — {anno_rif}")
mk_rif = mk[mk["anno"] == anno_rif]
if mk_rif.empty:
    mk_rif = mk[mk["anno"] == mk["anno"].max()]
mk_ult = mk_rif.nlargest(8, "n_dipendenti")
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

st.caption(
    "Dati: CNEL open data (Uniemens + Conto Annuale PA + Analisi Avanzata) · IODL v2.0. "
    f"Anno di riferimento {anno_rif}; il 2025 non include la PA."
)
