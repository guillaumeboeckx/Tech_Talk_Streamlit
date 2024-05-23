import pandas as pd
import geopandas as gpd
import folium
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st
from streamlit_folium import folium_static
import os


def fun_map(path_predicted):
    map = folium.Map(location=(52.5, 13.5), zoom_start=9.5)

    with st.form(key="map"):
        filenames_m = [f for f in os.listdir(path_predicted) if f.endswith(".gpkg")]
        campain_to_plot = st.selectbox("Campain to predict", filenames_m)

        if st.form_submit_button(label="Show predicted classes"):
            point_gdf = gpd.read_file(path_predicted + campain_to_plot)
            for i, row in point_gdf.iterrows():
                folium.Marker(location=(row["latitude"], row["longitude"]), icon=folium.Icon(color=row["class"], icon="star"), popup="Score: " + str(row["score"])).add_to(map)

    folium_static(map)
