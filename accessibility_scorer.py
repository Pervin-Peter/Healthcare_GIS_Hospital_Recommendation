# ============================================================
# PHASE 12 - HEALTHCARE ACCESSIBILITY SCORING
# ============================================================

import geopandas as gpd
import pandas as pd
from pathlib import Path


# ============================================================
# DATA PATHS
# ============================================================

BASE_DIR = Path(
    r"D:\SRM\Sem-3\GIS\Healthcare_GIS_Project"
)

HOSPITAL_FILE = (
    BASE_DIR
    / "Data"
    / "Final"
    / "cleanup"
    / "Hospital_Master_Final.csv"
)

BUS_FILE = (
    BASE_DIR
    / "Shapefiles"
    / "bus_stop"
    / "BusStops.shp"
)

RAILWAY_FILE = (
    BASE_DIR
    / "Shapefiles"
    / "RailwayStations"
    / "RailwayStations.shp"
)

CLINIC_FILE = (
    BASE_DIR
    / "Shapefiles"
    / "clinic"
    / "clinic.shp"
)

PHARMACY_FILE = (
    BASE_DIR
    / "Shapefiles"
    / "pharmacy"
    / "pharmacy.shp"
)


# ============================================================
# LOAD DATA
# ============================================================

def load_facility_data():

    print("Loading GIS facility datasets...")

    bus_stops = gpd.read_file(BUS_FILE)

    railway = gpd.read_file(RAILWAY_FILE)

    clinics = gpd.read_file(CLINIC_FILE)

    pharmacies = gpd.read_file(PHARMACY_FILE)

    print(f"Bus Stops       : {len(bus_stops)}")
    print(f"Railway Stations: {len(railway)}")
    print(f"Clinics         : {len(clinics)}")
    print(f"Pharmacies      : {len(pharmacies)}")

    return (
        bus_stops,
        railway,
        clinics,
        pharmacies
    )


# ============================================================
# HAVERSINE DISTANCE
# ============================================================

def haversine_vectorized(
    lat1,
    lon1,
    lat2,
    lon2
):
    """
    Calculate distance in kilometres
    using the Haversine formula.
    """

    import numpy as np

    R = 6371.0

    lat1 = np.radians(lat1)
    lon1 = np.radians(lon1)

    lat2 = np.radians(lat2)
    lon2 = np.radians(lon2)

    dlat = lat2 - lat1
    dlon = lon2 - lon1

    a = (
        np.sin(dlat / 2) ** 2
        +
        np.cos(lat1)
        *
        np.cos(lat2)
        *
        np.sin(dlon / 2) ** 2
    )

    c = 2 * np.arctan2(
        np.sqrt(a),
        np.sqrt(1 - a)
    )

    return R * c


# ============================================================
# FIND NEAREST FACILITY
# ============================================================

def nearest_facility_distance(
    hospital_lat,
    hospital_lon,
    facility_gdf
):

    facility_lat = facility_gdf.geometry.y.values
    facility_lon = facility_gdf.geometry.x.values

    distances = haversine_vectorized(
        hospital_lat,
        hospital_lon,
        facility_lat,
        facility_lon
    )

    return float(distances.min())


# ============================================================
# DISTANCE → SCORE
# ============================================================

def distance_to_score(
    distance_km,
    maximum_distance=5.0
):
    """
    Convert distance into accessibility score.

    0 km      = 100
    5 km or more = 0

    Linear scoring is used for transparency.
    """

    score = (
        100
        *
        (1 - distance_km / maximum_distance)
    )

    return max(
        0,
        min(
            100,
            score
        )
    )


# ============================================================
# MAIN ACCESSIBILITY CALCULATION
# ============================================================

def calculate_accessibility():

    print("\nLoading hospitals...")

    hospitals = pd.read_csv(
        HOSPITAL_FILE
    )

    print(
        f"Hospitals: {len(hospitals)}"
    )

    (
        bus_stops,
        railway,
        clinics,
        pharmacies
    ) = load_facility_data()

    results = []

    print(
        "\nCalculating accessibility..."
    )

    for index, hospital in hospitals.iterrows():

        try:

            hospital_lat = float(
                hospital["Latitude"]
            )

            hospital_lon = float(
                hospital["Longitude"]
            )

        except (
            ValueError,
            TypeError
        ):

            continue

        # ----------------------------------------------------
        # Nearest facilities
        # ----------------------------------------------------

        bus_distance = nearest_facility_distance(
            hospital_lat,
            hospital_lon,
            bus_stops
        )

        railway_distance = nearest_facility_distance(
            hospital_lat,
            hospital_lon,
            railway
        )

        clinic_distance = nearest_facility_distance(
            hospital_lat,
            hospital_lon,
            clinics
        )

        pharmacy_distance = nearest_facility_distance(
            hospital_lat,
            hospital_lon,
            pharmacies
        )

        # ----------------------------------------------------
        # Individual accessibility scores
        # ----------------------------------------------------

        bus_score = distance_to_score(
            bus_distance
        )

        railway_score = distance_to_score(
            railway_distance
        )

        clinic_score = distance_to_score(
            clinic_distance
        )

        pharmacy_score = distance_to_score(
            pharmacy_distance
        )

        # ----------------------------------------------------
        # Combined accessibility score
        # ----------------------------------------------------

        accessibility_score = (
            bus_score * 0.30
            +
            railway_score * 0.20
            +
            clinic_score * 0.20
            +
            pharmacy_score * 0.30
        )

        # ----------------------------------------------------
        # Store result
        # ----------------------------------------------------

        results.append({

            "Hospital":
                hospital.get(
                    "Hospital_Name",
                    "Unknown"
                ),

            "Latitude":
                hospital_lat,

            "Longitude":
                hospital_lon,

            "Nearest Bus Stop (km)":
                round(
                    bus_distance,
                    3
                ),

            "Nearest Railway Station (km)":
                round(
                    railway_distance,
                    3
                ),

            "Nearest Clinic (km)":
                round(
                    clinic_distance,
                    3
                ),

            "Nearest Pharmacy (km)":
                round(
                    pharmacy_distance,
                    3
                ),

            "Bus Accessibility Score":
                round(
                    bus_score,
                    2
                ),

            "Railway Accessibility Score":
                round(
                    railway_score,
                    2
                ),

            "Clinic Accessibility Score":
                round(
                    clinic_score,
                    2
                ),

            "Pharmacy Accessibility Score":
                round(
                    pharmacy_score,
                    2
                ),

            "Accessibility Score":
                round(
                    accessibility_score,
                    2
                )
        })

        # Progress
        if (index + 1) % 50 == 0:

            print(
                f"Processed {index + 1} hospitals..."
            )

    result_df = pd.DataFrame(
        results
    )

    # ========================================================
    # SAVE RESULT
    # ========================================================

    output_dir = (
        BASE_DIR
        / "Data"
        / "Final"
        / "cleanup"
    )

    output_dir.mkdir(
        parents=True,
        exist_ok=True
    )

    output_file = (
        output_dir
        / "Hospital_Accessibility_Score.csv"
    )

    result_df.to_csv(
        output_file,
        index=False
    )

    print(
        "\n======================================"
    )

    print(
        "ACCESSIBILITY CALCULATION COMPLETED"
    )

    print(
        "======================================"
    )

    print(
        f"Output: {output_file}"
    )

    print(
        f"Hospitals processed: {len(result_df)}"
    )

    print(
        "\nTop 10 hospitals by accessibility:"
    )

    print(
        result_df
        .sort_values(
            "Accessibility Score",
            ascending=False
        )
        .head(10)
        [
            [
                "Hospital",
                "Nearest Bus Stop (km)",
                "Nearest Railway Station (km)",
                "Nearest Clinic (km)",
                "Nearest Pharmacy (km)",
                "Accessibility Score"
            ]
        ]
        .to_string(index=False)
    )

    return result_df


# ============================================================
# RUN
# ============================================================

if __name__ == "__main__":

    calculate_accessibility()