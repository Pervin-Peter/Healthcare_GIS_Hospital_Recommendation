import pandas as pd


def dashboard():

    df = pd.read_csv("Data/Healthcare_Gap_Analysis.csv")

    print("\n" + "=" * 50)
    print("      HEALTHCARE GAP ANALYSIS DASHBOARD")
    print("=" * 50)

    print(f"Total Uncovered Facilities : {len(df)}")

    print("\nFacility Types")
    print(df["Facility Type"].value_counts())

    print("\nPriority")
    print(df["Priority"].value_counts())

    print("\nAverage Distance")
    print(round(df["Distance (km)"].mean(), 2), "km")

    print("\nMaximum Distance")
    print(round(df["Distance (km)"].max(), 2), "km")

    print("\nMinimum Distance")
    print(round(df["Distance (km)"].min(), 2), "km")