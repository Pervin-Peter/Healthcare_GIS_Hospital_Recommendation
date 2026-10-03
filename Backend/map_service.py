import folium
from Backend.data_loader import *
from folium.plugins import MarkerCluster


def create_map(patient_lat=None, patient_lon=None, recommendations=None):

    hospitals = load_hospitals()
    busstops = load_busstops()
    clinics = load_clinics()
    pharmacy = load_pharmacy()
    railway = load_railway()
    recommendation_zones = load_recommendations()

    # Chennai Center
    m = folium.Map(
        location=[13.0827, 80.2707],
        zoom_start=11
    )
# -----------------------------
# Feature Groups
# -----------------------------
    hospital_group = folium.FeatureGroup(name="Hospitals")
    busstop_group = folium.FeatureGroup(name="Bus Stops")
    clinic_group = folium.FeatureGroup(name="Clinics")
    pharmacy_group = folium.FeatureGroup(name="Pharmacy")
    railway_group = folium.FeatureGroup(name="Railway Stations")
    recommendation_group = folium.FeatureGroup(name="Recommended Hospitals")

    # Marker Clusters
    hospital_cluster = MarkerCluster().add_to(hospital_group)
    busstop_cluster = MarkerCluster().add_to(busstop_group)
    clinic_cluster = MarkerCluster().add_to(clinic_group)
    pharmacy_cluster = MarkerCluster().add_to(pharmacy_group)
    railway_cluster = MarkerCluster().add_to(railway_group)
    # -----------------------------
    # Hospitals
    # -----------------------------
    for _, row in hospitals.iterrows():

        folium.CircleMarker(
            location=[row["Latitude"], row["Longitude"]],
            radius=6,
            color="red",
            fill=True,
            fill_color="red",
            popup=f"""
            <b>Hospital</b><br>
            Name: {row['Hospital_Name']}<br>
            Latitude: {row['Latitude']}<br>
            Longitude: {row['Longitude']}
            """
        ).add_to(hospital_cluster)

    # -----------------------------
    # Bus Stops
    # -----------------------------
    for _, row in busstops.iterrows():

        folium.CircleMarker(
            location=[row["Latitude"], row["Longitude"]],
            radius=4,
            color="blue",
            fill=True,
            fill_color="blue",
            popup=row["name"]
        ).add_to(busstop_cluster)

    # -----------------------------
    # Clinics
    # -----------------------------
    for _, row in clinics.iterrows():

        folium.CircleMarker(
            location=[row["Latitude"], row["Longitude"]],
            radius=4,
            color="orange",
            fill=True,
            fill_color="orange",
            popup=row["name"]
        ).add_to(clinic_cluster)

    # -----------------------------
    # Pharmacy
    # -----------------------------
    for _, row in pharmacy.iterrows():

        folium.CircleMarker(
            location=[row["Latitude"], row["Longitude"]],
            radius=4,
            color="green",
            fill=True,
            fill_color="green",
            popup=row["name"]
        ).add_to(pharmacy_cluster)

    # -----------------------------
    # Railway
    # -----------------------------
    for _, row in railway.iterrows():

        folium.CircleMarker(
            location=[row["Latitude"], row["Longitude"]],
            radius=5,
            color="black",
            fill=True,
            fill_color="black",
            popup=row["name"]
        ).add_to(railway_cluster)

# -----------------------------
# Recommended Hospital Zones
# -----------------------------
    for _, row in recommendation_zones.iterrows():

        folium.Marker(
        location=[row["Latitude"], row["Longitude"]],
        popup=f"""
        <b>Recommended Hospital</b><br>
        Zone: {row["Zone"]}<br>
        Facilities: {row["Facilities"]}<br>
        Avg Distance: {row["Average_Distance"]:.2f} km<br>
        Score: {row["Recommendation Score"]:.2f}<br>
        Recommendation: {row["Recommendation"]}
        """,
        icon=folium.Icon(
            color="purple",
            icon="plus",
            prefix="fa"
        )
    ).add_to(recommendation_group)


# Add Feature Groups
    hospital_group.add_to(m)
    busstop_group.add_to(m)
    clinic_group.add_to(m)
    pharmacy_group.add_to(m)
    railway_group.add_to(m)
    recommendation_group.add_to(m)
    # -----------------------------
# Recommended Hospital Zones
# -----------------------------
# -----------------------------
# Patient Location
# -----------------------------
    if patient_lat is not None and patient_lon is not None:

        folium.Marker(
            location=[patient_lat, patient_lon],
            popup="Patient Location",
            icon=folium.Icon(
                color="blue",
                icon="user",
                prefix="fa"
            )
        ).add_to(m)

        # -----------------------------
# Recommended Hospitals
# -----------------------------
    if recommendations is not None:

        for _, row in recommendations.iterrows():

            folium.Marker(
                location=[row["Latitude"], row["Longitude"]],
                popup=f"""
                <b>{row['Hospital']}</b><br>
                Distance : {row['Distance (km)']} km
                """,
                icon=folium.Icon(
                    color="green",
                    icon="plus",
                    prefix="fa"
                )
            ).add_to(m)

    # Layer Control
    folium.LayerControl().add_to(m)

    
    return m