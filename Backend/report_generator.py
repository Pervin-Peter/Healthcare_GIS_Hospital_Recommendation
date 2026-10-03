import pandas as pd


def generate_master_report():

    # Read all gap analysis files
    bus = pd.read_csv("Data/BusStop_Gap_Analysis.csv")
    clinic = pd.read_csv("Data/Clinic_Gap_Analysis.csv")
    pharmacy = pd.read_csv("Data/Pharmacy_Gap_Analysis.csv")
    railway = pd.read_csv("Data/Railway_Gap_Analysis.csv")

    # Combine all datasets
    master = pd.concat(
        [bus, clinic, pharmacy, railway],
        ignore_index=True
    )

    # Sort by distance (largest first)
    master = master.sort_values(
        by="Distance (km)",
        ascending=False
    )

    # Save master report
    master.to_csv(
        "Data/Healthcare_Gap_Analysis.csv",
        index=False
    )

    print("\nHealthcare_Gap_Analysis.csv Created Successfully.")
    print("Total Records :", len(master))