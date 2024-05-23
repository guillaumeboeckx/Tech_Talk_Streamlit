import geopandas as gpd
import streamlit as st
import os
from utils import generate_grid, enrich_grid, predict_class


def fun_pipeline(path_grid, path_enriched, path_predicted):

    st.header("Step 1: Create a grid of points")

    with st.form(key="grid"):
        name_campain = st.text_input("Name of the campain")
        lat_min = st.number_input("MIN Latitude (lower left corner)")
        lon_min = st.number_input("MIN Longitude (lower left corner)")
        lat_max = st.number_input("MAX Latitude (upper right corner)")
        lon_max = st.number_input("MAX Longitude (upper right corner)")
        n_lat = st.number_input("Number of rows in the grid", min_value=2, max_value=100, value=5)
        n_lon = st.number_input("Number of columns in the grid", min_value=2, max_value=100, value=5)

        if st.form_submit_button(label="Generate grid"):
            if (lat_min == lat_max) | (lat_min == lat_max):
                st.warning("Warning: minimum and maximum coordinates cannot be equal")
            else:
                point_gdf = generate_grid(lat_min, lon_min, lat_max, lon_max, n_lat, n_lon)
                point_gdf.to_file(path_grid + name_campain + ".gpkg")
                st.write(name_campain + " created")


    st.header("Step 2: Enrich the grid with open data")

    with st.form(key="enrich"):
        filenames_1 = [f for f in os.listdir(path_grid) if f.endswith(".gpkg")]
        campain_to_enrich = st.selectbox("Campain to enrich", filenames_1)

        if st.form_submit_button(label="Enrich grid"):
            point_gdf = gpd.read_file(path_grid + campain_to_enrich)
            point_gdf = enrich_grid(point_gdf)
            point_gdf.to_file(path_enriched + campain_to_enrich)
            st.write(campain_to_enrich + " enriched")


    st.header("Step 3: Predict the classes of the points")

    with st.form(key="predict"):
        filenames_2 = [f for f in os.listdir(path_enriched) if f.endswith(".gpkg")]
        campain_to_predict = st.selectbox("Campain to predict", filenames_2)

        if st.form_submit_button(label="Predict classes"):
            point_gdf = gpd.read_file(path_enriched + campain_to_predict)
            point_gdf = predict_class(point_gdf)
            point_gdf.to_file(path_predicted + campain_to_predict)
            st.write(campain_to_predict + " predicted")