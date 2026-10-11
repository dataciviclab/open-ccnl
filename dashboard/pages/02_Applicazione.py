"""Applicazione — quote, serie e mercati nel tempo."""

import plotly.express as px
import streamlit as st

from sources import SLUG_APPLICAZIONE, fmt_num, intelligence, mercati, query_clean

st.title("👥 Applicazione dei CCNL")

df = intelligence()
with_dip = df[df["n_dipendenti"].fillna(0) > 0].copy()

tab1, tab2, tab3 = st.tabs(["Quota F/M", "Serie storica", "Mercati nel tempo"])

with tab1:
    st.subheader("Quota di donne per CCNL (top 20 per dipendenti)")
    top20 = with_dip.nlargest(20, "n_dipendenti").dropna(subset=["quota_dipendenti_f"])
    fig = px.bar(
        top20.sort_values("quota_dipendenti_f"),
        x="quota_dipendenti_f",
        y="titolo",
        orientation="h",
        custom_data=["codice_ccnl", "n_dipendenti"],
    )
    fig.update_layout(
        height=560,
        margin={"t": 10, "b": 30},
        showlegend=False,
        xaxis_tickformat=".0%",
    )
    fig.update_traces(
        marker_color="#6366f1",
        hovertemplate="<b>%{customdata[0]}</b><br>quote F: %{x:.1%}<br>dipendenti: %{customdata[1]:,.0f}<extra></extra>",
    )
    st.plotly_chart(fig, width="stretch")
    st.caption("Solo CCNL con dato F/M disponibile (dal 2023).")

with tab2:
    st.subheader("Dipendenti totali per anno")
    serie = query_clean(
        SLUG_APPLICAZIONE,
        """
        SELECT anno, sum(n_dipendenti) AS n_dipendenti
        FROM clean_input
        GROUP BY anno
        ORDER BY anno
        """,
    )
    if serie.empty:
        st.info("Serie non disponibile.")
    else:
        fig2 = px.line(serie, x="anno", y="n_dipendenti", markers=True)
        fig2.update_layout(height=360, margin={"t": 10, "b": 30}, yaxis_tickformat=",")
        fig2.update_traces(line_color="#6366f1", hovertemplate="%{y:,.0f}<extra></extra>")
        st.plotly_chart(fig2, width="stretch")
        st.caption(
            f"Totale ultimo anno ({int(serie['anno'].max())}): "
            f"{fmt_num(int(serie['n_dipendenti'].max()))} dipendenti · "
            "2025 può essere parziale."
        )

with tab3:
    st.subheader("Dipendenti per sottosezione, 2018–2025")
    mk = mercati()
    # esclude il contenitore generico "vigenti o ultrattivi" e le righe a zero
    mkf = mk[
        ~mk["sottosezione"].isin(
            ["CCNL settore vigenti o ultrattivi", "altri CCNL", "CCNL di nuovo deposito"]
        )
        & (mk["n_dipendenti"] > 0)
    ].copy()
    top_settori = (
        mkf[mkf["anno"] == mkf["anno"].max()]
        .nlargest(6, "n_dipendenti")["sottosezione"]
        .tolist()
    )
    mkf = mkf[mkf["sottosezione"].isin(top_settori)]
    # plotly collega i punti nell'ordine delle righe: serve sort esplicito
    mkf = mkf.sort_values(["sottosezione", "anno"])
    fig3 = px.line(
        mkf,
        x="anno",
        y="n_dipendenti",
        color="sottosezione",
        markers=True,
    )
    fig3.update_layout(height=420, margin={"t": 10, "b": 30}, yaxis_tickformat=",")
    st.plotly_chart(fig3, width="stretch")
    st.caption("Top 6 sottosezioni per dipendenti nell'ultimo anno (esclusi contenitori generici).")
