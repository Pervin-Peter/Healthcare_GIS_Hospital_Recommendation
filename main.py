from Backend.map_service import create_map
from Backend.gap_analysis import healthcare_gap_analysis
from Backend.report_generator import generate_master_report
from Backend.dashboard import dashboard
from Backend.charts import generate_charts
from Backend.recommendation import generate_recommendation_zones
from Backend.hospital_recommender import recommend_hospitals

healthcare_gap_analysis()

generate_master_report()

dashboard()

generate_charts()

generate_recommendation_zones()

print("\n")
print("=" * 60)
print("PATIENT LOCATION")
print("=" * 60)

patient_lat = float(input("Enter Patient Latitude : "))
patient_lon = float(input("Enter Patient Longitude : "))

recommendations = recommend_hospitals(
    patient_lat,
    patient_lon
)

m = create_map(
    patient_lat,
    patient_lon,
    recommendations
)

m.save("Maps/Healthcare_Map.html")

print("Map Created Successfully")

print("\n")
print("=" * 60)
print("AI HOSPITAL RECOMMENDATION")
print("=" * 60)

recommendations = recommend_hospitals(
    13.0827,
    80.2707
)

print(recommendations)