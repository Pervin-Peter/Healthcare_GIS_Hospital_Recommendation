import pandas as pd
import geopandas as gpd
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parent.parent

DATA_DIR = BASE_DIR / "Data" / "Final" / "cleanup"

SHAPEFILE_DIR = (
    BASE_DIR
    / "Shapefiles"
)


def load_hospitals():

    return pd.read_csv(
        DATA_DIR / "Hospital_Master_Final.csv"
    )


def load_busstops():

    path = (
        SHAPEFILE_DIR
        / "bus_stop"
        / "BusStops.shp"
    )

    gdf = gpd.read_file(path)

    gdf = gdf.to_crs(epsg=4326)

    gdf["Latitude"] = gdf.geometry.y
    gdf["Longitude"] = gdf.geometry.x

    return pd.DataFrame(gdf.drop(columns="geometry"))


def load_clinics():

    path = (
        SHAPEFILE_DIR
        / "clinic"
        / "clinic.shp"
    )

    gdf = gpd.read_file(path)

    gdf = gdf.to_crs(epsg=4326)

    gdf["Latitude"] = gdf.geometry.y
    gdf["Longitude"] = gdf.geometry.x

    return pd.DataFrame(gdf.drop(columns="geometry"))


def load_pharmacy():

    path = (
        SHAPEFILE_DIR
        / "pharmacy"
        / "pharmacy.shp"
    )

    gdf = gpd.read_file(path)

    gdf = gdf.to_crs(epsg=4326)

    gdf["Latitude"] = gdf.geometry.y
    gdf["Longitude"] = gdf.geometry.x

    return pd.DataFrame(gdf.drop(columns="geometry"))


def load_railway():

    path = (
        SHAPEFILE_DIR
        / "RailwayStations"
        / "RailwayStations.shp"
    )

    gdf = gpd.read_file(path)

    gdf = gdf.to_crs(epsg=4326)

    gdf["Latitude"] = gdf.geometry.y
    gdf["Longitude"] = gdf.geometry.x

    return pd.DataFrame(gdf.drop(columns="geometry"))


def load_recommendations():

    return pd.read_csv(
        DATA_DIR / "Recommended_Hospital_Zones.csv"
    )