import streamlit as st
from tabs.pipeline import fun_pipeline
from tabs.map import fun_map

# points used for true project : [12.96, 52.29, 13.76, 52.68, 36, 28] # inverser lat et lon

path_grid = "data/grid/"
path_enriched = "data/enriched/"
path_predicted = "data/predicted/"

st.title("GIS Prospection Tool")

tab_pipeline, tab_map = st.tabs(["Pipeline", "Map"])

with tab_pipeline:
    fun_pipeline(path_grid, path_enriched, path_predicted)

with tab_map:
    fun_map(path_predicted)

