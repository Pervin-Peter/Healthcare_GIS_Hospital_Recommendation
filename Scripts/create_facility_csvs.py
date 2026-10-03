import geopandas as gpd
import pandas as pd
from pathlib import Path


# =========================================================
# PROJECT DIRECTORIES
# =========================================================

BASE_DIR = Path(__file__).resolve().parent.parent

SHAPEFILE_DIR = BASE_DIR / "Shapefiles"

OUTPUT_DIR = BASE_DIR / "Data" / "Final" / "cleanup"

OUTPUT_DIR.mkdir(
    parents=True,
    exist_ok=True
)


# =========================================================
# SOURCE SHAPEFILES
# =========================================================

FACILITIES = {

    "BusStops": (
        SHAPEFILE_DIR
        / "bus_stop"
        / "BusStops.shp"
    ),

    "Clinics": (
        SHAPEFILE_DIR
        / "clinic"
        / "clinic.shp"
    ),

    "Pharmacy": (
        SHAPEFILE_DIR
        / "pharmacy"
        / "pharmacy.shp"
    ),

    "RailwayStations": (
        SHAPEFILE_DIR
        / "RailwayStations"
        / "RailwayStations.shp"
    )
}


# =========================================================
# PROCESS FACILITIES
# =========================================================

for facility_name, shapefile_path in FACILITIES.items():

    print()
    print("=" * 60)
    print(f"Processing: {facility_name}")
    print("=" * 60)

    if not shapefile_path.exists():

        print("ERROR: Shapefile not found:")
        print(shapefile_path)

        continue

    try:

        # Read shapefile
        gdf = gpd.read_file(
            shapefile_path
        )

        print(
            f"Records loaded: {len(gdf)}"
        )

        print(
            f"Original CRS: {gdf.crs}"
        )

        # Convert to WGS84
        if gdf.crs is not None:

            gdf = gdf.to_crs(
                epsg=4326
            )

        # Extract coordinates
        gdf["Latitude"] = (
            gdf.geometry.y
        )

        gdf["Longitude"] = (
            gdf.geometry.x
        )

        # Remove geometry
        df = pd.DataFrame(
            gdf.drop(
                columns=["geometry"]
            )
        )

        # Output file
        output_file = (
            OUTPUT_DIR
            / f"{facility_name}_Full.csv"
        )

        # Save CSV
        df.to_csv(
            output_file,
            index=False
        )

        print(
            f"Saved: {output_file}"
        )

        print(
            f"Final records: {len(df)}"
        )

        print(
            f"Latitude range: "
            f"{df['Latitude'].min()} -> "
            f"{df['Latitude'].max()}"
        )

        print(
            f"Longitude range: "
            f"{df['Longitude'].min()} -> "
            f"{df['Longitude'].max()}"
        )

        print(
            "Coordinate columns added: "
            "Latitude, Longitude"
        )

    except Exception as e:

        print(
            f"ERROR processing {facility_name}:"
        )

        print(e)


print()
print("=" * 60)
print("FACILITY CSV GENERATION COMPLETED")
print("=" * 60)