import pandas as pd
from sklearn.cluster import KMeans


def generate_recommendation_zones():

    df = pd.read_csv("Data/Healthcare_Gap_Analysis.csv")

    coordinates = df[["Latitude", "Longitude"]]

    kmeans = KMeans(
        n_clusters=5,
        random_state=42,
        n_init=10
    )

    df["Zone"] = kmeans.fit_predict(coordinates)

    summary = (
        df.groupby("Zone")
        .agg(
            Facilities=("Facility Name", "count"),
            Average_Distance=("Distance (km)", "mean"),
            High_Priority=("Priority", lambda x: (x == "High").sum()),
            Latitude=("Latitude", "mean"),
            Longitude=("Longitude", "mean")
        )
        .reset_index()
    )

    # AI Recommendation Score
    summary["Recommendation Score"] = (
        summary["Facilities"] * 2 +
        summary["Average_Distance"] * 10 +
        summary["High_Priority"] * 15
    )

    summary["Recommendation"] = summary[
        "Recommendation Score"
    ].apply(
        lambda score:
        "Immediate Hospital"
        if score >= 80
        else "High Priority"
        if score >= 60
        else "Future Expansion"
    )

    summary = summary.sort_values(
        "Recommendation Score",
        ascending=False
    )

    summary.to_csv(
    "Data/Final/cleanup/Recommended_Hospital_Zones.csv",
    index=False
    )

    print("Recommended_Hospital_Zones.csv Created Successfully.")