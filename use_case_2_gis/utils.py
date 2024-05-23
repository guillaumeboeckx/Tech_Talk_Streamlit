import pandas as pd
import geopandas as gpd
from shapely.geometry import Point
from random import random

def generate_grid(lat_min, lon_min, lat_max, lon_max, n_lat, n_lon):

    width_lat = (lat_max - lat_min) / (n_lat-1)
    width_lon = (lon_max - lon_min) / (n_lon-1)
    ind = 0
    point_set = []
    for i in range(n_lat):
        for j in range(n_lon):
            point_set.append([ind, lat_min+i*width_lat, lon_min+j*width_lon, Point(lat_min+i*width_lat, lon_min+j*width_lon)])
            ind += 1
    
    point_df = pd.DataFrame(point_set, columns=["point_id", "latitude", "longitude", "geometry"])
    point_gdf = gpd.GeoDataFrame(point_df, geometry="geometry")
    
    return point_gdf


def enrich_grid(gdf):
    gdf["score"] = 0
    gdf["score"] = gdf["score"].apply(lambda x: random())
    
    return gdf


def predict_class(gdf):
    gdf["class"] = "red"
    gdf.loc[gdf["score"] > 0.5, "class"] = "green"
    return gdf
