import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd

st.set_page_config(layout="wide")

@st.cache_data
def get_df():
    return pd.read_excel("Journal comptable total.xlsx")

def get_metric(df, year):
    bplus_1 = df[(df["année"] == "2021-2022") & (df["direction"] == "recettes")]["montant_abs"].sum()
    bmoins_1 = df[(df["année"] == "2021-2022") & (df["direction"] == "dépenses")]["montant_abs"].sum()
    btot_1 = bplus_1 - bmoins_1

    bplus_2 = df[(df["année"] == "2022-2023") & (df["direction"] == "recettes")]["montant_abs"].sum()
    bmoins_2 = df[(df["année"] == "2022-2023") & (df["direction"] == "dépenses")]["montant_abs"].sum()
    btot_2 = bplus_2 - bmoins_2

    bplus_3 = df[(df["année"] == "2023-2024") & (df["direction"] == "recettes")]["montant_abs"].sum()
    bmoins_3 = df[(df["année"] == "2023-2024") & (df["direction"] == "dépenses")]["montant_abs"].sum()
    btot_3 = bplus_3 - bmoins_3
    
    montant_origine = 7110

    if year == "2021-2022":        
        return [montant_origine, montant_origine + btot_1, btot_1, bplus_1, 0, bmoins_1, 0]
    elif year == "2022-2023":
        return [montant_origine + btot_1, montant_origine + btot_1 + btot_2, btot_2, bplus_2, bplus_2 - bplus_1, bmoins_2, bmoins_2 - bmoins_1]
    elif year == "2023-2024":
        return [montant_origine + btot_1 + btot_2, montant_origine + btot_1 + btot_2 + btot_3, btot_3, bplus_3, bplus_3 - bplus_2, bmoins_3, bmoins_3 - bmoins_2]
    else:
        return [0,0,0,0,0,0]
        
# select parameters
col_para = st.columns([4,1,2,1,2,1])
with col_para[0]:
    st.title("Rapport Comptabilité")
with col_para[2]:
    year = st.selectbox("Année comptable", ["2021-2022", "2022-2023", "2023-2024"])
with col_para[4]:
    direction = st.selectbox("Recettes ou dépenses", ["recettes", "dépenses"])

st.divider()
col1, col_vide, col2 = st.columns([6,1,4])

with col1:
    # section 0: some indicators
    col1_1, col1_2, col1_3 = st.columns(3)
    df = get_df()
    [v0, v1, d1, v2, d2, v3, d3] = get_metric(df, year)
    with col1_1:
        st.metric(label="État des comptes", value=round(v1, 2), delta=round(d1, 2))
    with col1_2:
        st.metric(label="Recettes", value=round(v2, 2), delta=round(d2, 2))
    with col1_3:
        st.metric(label="Dépenses", value=round(v3, 2), delta=round(d3, 2))

    # graph 1: état des comptes par mois
    df_1 = get_df()
    df_1 = df_1[df_1["année"] == year].groupby("mois").agg({"montant" : "sum"}).reset_index()
    l_1 = df_1["montant"].tolist()
    
    fig_1 = go.Figure(go.Waterfall(
        x = ["Ouverture", "Juillet", "Aout", "Septembre", "Octobre", "Novembre", "Décembre", 
            "Janvier", "Février", "Mars", "Avril", "Mai", "Juin", "Cloture"],
        measure = ["absolute", "relative", "relative", "relative", "relative", "relative", "relative",
                   "relative", "relative", "relative", "relative", "relative", "relative", "total"],
        y = [v0] + l_1 + [0]
    ))
    fig_1.update_layout(title="État des comptes par mois")
    st.plotly_chart(fig_1, use_container_width=True)
    
    # graph 2: montant par catégorie par ans
    df_2 = get_df()
    df_2 = df_2.groupby(["catégorie", "année"]).agg({"montant" : "sum"}).reset_index()
    fig_2 = px.bar(df_2, x="catégorie", y="montant", color="année", barmode = 'group', title="Montant par catégorie par ans")
    st.plotly_chart(fig_2, use_container_width=True)

with col2:
    # graph 3: recettes/dépenses par categories (pour 1 ans)
    st.subheader("Année " + year)
    df_3 = get_df()
    df_3 = df_3[(df_3["année"] == year) & (df_3["direction"] == direction)]
    fig_3 = px.pie(df_3, values="montant_abs", names="catégorie")
    st.plotly_chart(fig_3, use_container_width=True)
    
    # graph 4: recettes/dépenses par categories (pour les 3 ans)
    st.subheader("Total des 3 ans")
    df_4 = get_df()
    df_4 = df_4[df_4["direction"] == direction]
    fig_4 = px.pie(df_4, values="montant_abs", names="catégorie")
    st.plotly_chart(fig_4, use_container_width=True)
