import pandas as pd
from math import radians, sin, cos, sqrt, atan2
from Backend.data_loader import (
    load_hospitals,
    load_busstops,
    load_clinics,
    load_pharmacy,
    load_railway
)
def haversine(lat1, lon1, lat2, lon2):
    """
    Calculate distance between two latitude/longitude points in KM.
    """

    R = 6371

    dlat = radians(lat2 - lat1)
    dlon = radians(lon2 - lon1)

    a = (
        sin(dlat / 2) ** 2
        + cos(radians(lat1))
        * cos(radians(lat2))
        * sin(dlon / 2) ** 2
    )

    c = 2 * atan2(sqrt(a), sqrt(1 - a))

    return R * c

def analyze_gap(facilities, hospitals, facility_type, output_file):

    gap_results = []

    for _, facility in facilities.iterrows():

        nearest_distance = float("inf")
        nearest_hospital = ""

        for _, hospital in hospitals.iterrows():

            distance = haversine(
                facility["Latitude"],
                facility["Longitude"],
                hospital["Latitude"],
                hospital["Longitude"]
            )

            if distance < nearest_distance:
                nearest_distance = distance
                nearest_hospital = hospital["Hospital_Name"]

        # Handle missing names
        facility_name = facility["name"]

        if pd.isna(facility_name):
            facility_name = f"Unnamed {facility_type}"

        # Priority
        if nearest_distance <= 1:
            priority = "Low"
        elif nearest_distance <= 3:
            priority = "Medium"
        else:
            priority = "High"

        gap_results.append({
            "Facility Type": facility_type,
            "Facility Name": facility_name,
            "Latitude": facility["Latitude"],
            "Longitude": facility["Longitude"],
            "Nearest Hospital": nearest_hospital,
            "Distance (km)": round(nearest_distance, 2),
            "Priority": priority
        })

    gap_df = pd.DataFrame(gap_results)

    gap_df.to_csv(
        f"Data/{output_file}",
        index=False
    )

    print(f"{output_file} Created Successfully.")

def healthcare_gap_analysis():

    hospitals = load_hospitals()
    busstops = load_busstops()
    clinics = load_clinics()
    pharmacy = load_pharmacy()
    railway = load_railway()

    print("\nGenerating Healthcare Gap Analysis...")
    print("-" * 50)

    analyze_gap(
        busstops,
        hospitals,
        "Bus Stop",
        "BusStop_Gap_Analysis.csv"
    )

    analyze_gap(
        clinics,
        hospitals,
        "Clinic",
        "Clinic_Gap_Analysis.csv"
    )

    analyze_gap(
        pharmacy,
        hospitals,
        "Pharmacy",
        "Pharmacy_Gap_Analysis.csv"
    )

    analyze_gap(
        railway,
        hospitals,
        "Railway Station",
        "Railway_Gap_Analysis.csv"
    )

    print("-" * 50)
    print("Healthcare Gap Analysis Completed Successfully!")

    print("Hospitals :", len(hospitals))
    print("Bus Stops :", len(busstops))
    print("Clinics :", len(clinics))
    print("Pharmacy :", len(pharmacy))
    print("Railway :", len(railway))