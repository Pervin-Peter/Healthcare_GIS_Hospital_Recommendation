import pandas as pd
import matplotlib.pyplot as plt


def generate_charts():

    df = pd.read_csv("Data/Healthcare_Gap_Analysis.csv")

    # ============================================
    # Chart 1 - Facility Type Distribution
    # ============================================

    plt.figure(figsize=(8,5))

    df["Facility Type"].value_counts().plot(kind="bar")

    plt.title("Facility Type Distribution")
    plt.xlabel("Facility Type")
    plt.ylabel("Count")

    plt.tight_layout()

    plt.savefig("Charts/Facility_Type_Distribution.png")

    plt.close()

    print("Facility Type Chart Created.")

    # ============================================
    # Chart 2 - Priority Distribution
    # ============================================

    plt.figure(figsize=(6,6))

    df["Priority"].value_counts().plot(
        kind="pie",
        autopct="%1.1f%%"
    )

    plt.ylabel("")

    plt.title("Priority Distribution")

    plt.tight_layout()

    plt.savefig("Charts/Priority_Distribution.png")

    plt.close()

    print("Priority Chart Created.")

    # ============================================
    # Chart 3 - Distance Distribution
    # ============================================

    plt.figure(figsize=(8,5))

    plt.hist(
        df["Distance (km)"],
        bins=10
    )

    plt.title("Distance Distribution")

    plt.xlabel("Distance (km)")

    plt.ylabel("Number of Facilities")

    plt.tight_layout()

    plt.savefig("Charts/Distance_Distribution.png")

    plt.close()

    print("Distance Distribution Chart Created.")

    # ============================================
    # Chart 4 - Top 10 Longest Gaps
    # ============================================

    top10 = df.nlargest(10, "Distance (km)")

    plt.figure(figsize=(10,6))

    plt.barh(
        top10["Facility Name"],
        top10["Distance (km)"]
    )

    plt.title("Top 10 Longest Healthcare Gaps")

    plt.xlabel("Distance (km)")

    plt.tight_layout()

    plt.savefig("Charts/Top10_Gap_Locations.png")

    plt.close()

    print("Top 10 Gap Chart Created.")