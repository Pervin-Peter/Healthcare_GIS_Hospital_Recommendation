import pandas as pd
import math
import re
from pathlib import Path

from Backend.data_loader import load_hospitals


# =========================================================
# PATHS
# =========================================================

BASE_DIR = Path(__file__).resolve().parent.parent

ACCESSIBILITY_FILE = (
    BASE_DIR
    / "Data"
    / "Final"
    / "cleanup"
    / "Hospital_Accessibility_Score.csv"
)


# =========================================================
# BASIC HELPERS
# =========================================================

def clean_text(value):
    """
    Convert a value into normalized lowercase text.
    """
    if pd.isna(value):
        return ""

    return str(value).strip().lower()


def is_yes(value):
    """
    Check whether a field represents Yes/True.
    """
    value = clean_text(value)

    return value in [
        "yes",
        "true",
        "1",
        "y"
    ]


# =========================================================
# HAVERSINE DISTANCE
# =========================================================

def haversine_distance(
    lat1,
    lon1,
    lat2,
    lon2
):
    """
    Calculate distance between two latitude/longitude
    coordinates in kilometres.
    """

    R = 6371.0

    lat1 = math.radians(lat1)
    lon1 = math.radians(lon1)

    lat2 = math.radians(lat2)
    lon2 = math.radians(lon2)

    dlat = lat2 - lat1
    dlon = lon2 - lon1

    a = (
        math.sin(dlat / 2) ** 2
        +
        math.cos(lat1)
        *
        math.cos(lat2)
        *
        math.sin(dlon / 2) ** 2
    )

    c = 2 * math.atan2(
        math.sqrt(a),
        math.sqrt(1 - a)
    )

    return R * c


# =========================================================
# DISTANCE SCORE
# =========================================================

def calculate_distance_score(distance_km):

    """
    Convert distance into a 0-100 score.

    0 km  = 100
    10 km = 0

    This is a transparent rule-based normalization.
    """

    score = 100 * (
        1 - distance_km / 10.0
    )

    return round(
        max(0, min(100, score)),
        2
    )


# =========================================================
# EMERGENCY SCORE
# =========================================================

def calculate_emergency_score(value):

    if is_yes(value):
        return 100

    return 0


# =========================================================
# HEALTHCARE TYPE SCORE
# =========================================================

def calculate_healthcare_type_score(value):

    value = clean_text(value)

    if value == "hospital":
        return 100

    if value in [
        "clinic",
        "health centre",
        "health center"
    ]:
        return 70

    if value:
        return 50

    return 0


# =========================================================
# LOAD ACCESSIBILITY SCORES
# =========================================================

def load_accessibility_scores():

    """
    Load the real GIS-based accessibility scores.

    Matching is done using latitude/longitude instead of
    hospital name because some hospitals have missing names.
    """

    if not ACCESSIBILITY_FILE.exists():

        print(
            "WARNING: Accessibility file not found:",
            ACCESSIBILITY_FILE
        )

        return {}

    accessibility_df = pd.read_csv(
        ACCESSIBILITY_FILE
    )

    lookup = {}

    for _, row in accessibility_df.iterrows():

        try:

            lat = round(
                float(row["Latitude"]),
                6
            )

            lon = round(
                float(row["Longitude"]),
                6
            )

            score = float(
                row["Accessibility Score"]
            )

            lookup[
                (lat, lon)
            ] = score

        except Exception:

            continue

    print(
        "Accessibility scores loaded:",
        len(lookup)
    )

    return lookup


# =========================================================
# SPECIALTY KEYWORDS
# =========================================================

SPECIALTY_KEYWORDS = {

    "dental": [
        "dental",
        "dentist",
        "dentistry",
        "tooth",
        "oral",
        "maxillofacial"
    ],

    "orthopaedic": [
        "orthopaedic",
        "orthopedic",
        "orthopaedics",
        "orthopedics",
        "bone",
        "joint"
    ],

    "cardiology": [
        "cardiology",
        "cardiac",
        "cardio",
        "heart"
    ],

    "neurology": [
        "neurology",
        "neurological",
        "neuro",
        "brain"
    ],

    "ophthalmology": [
        "ophthalmology",
        "ophthalmic",
        "eye",
        "vision",
        "ophthalm"
    ],

    "oncology": [
        "oncology",
        "oncological",
        "cancer",
        "tumor",
        "tumour"
    ],

    "paediatrics": [
        "paediatric",
        "paediatrics",
        "pediatric",
        "pediatrics",
        "child",
        "children"
    ],

    "gynaecology": [
        "gynaecology",
        "gynaecologist",
        "gynecology",
        "gynecologist",
        "obstetrics",
        "maternity",
        "maternity hospital"
    ],

    "ent": [
        "ent",
        "ear nose throat",
        "otorhinolaryngology",
        "otolaryngology"
    ],

    "dermatology": [
        "dermatology",
        "dermatologist",
        "skin"
    ],

    "psychiatry": [
        "psychiatry",
        "psychiatric",
        "psychiatrist",
        "mental health",
        "schizophrenia"
    ],

    "general surgery": [
        "general surgery",
        "surgeon",
        "surgical"
    ],

    "urology": [
        "urology",
        "urological",
        "uro",
        "kidney"
    ],

    "gastroenterology": [
        "gastroenterology",
        "gastro",
        "digestive"
    ],

    "pulmonology": [
        "pulmonology",
        "pulmonary",
        "lung",
        "respiratory"
    ]
}


# =========================================================
# SPECIALTY MATCHING
# =========================================================

def calculate_specialty_match(
    hospital_name,
    hospital_specialty,
    requested_specialty
):

    requested = clean_text(
        requested_specialty
    )

    hospital_name = clean_text(
        hospital_name
    )

    hospital_specialty = clean_text(
        hospital_specialty
    )

    # -----------------------------------------------------
    # GENERAL / ANY SPECIALTY
    # -----------------------------------------------------

    if requested in [
        "",
        "general",
        "general / any specialty",
        "any",
        "any specialty"
    ]:

        return 50


    # -----------------------------------------------------
    # GET KEYWORDS
    # -----------------------------------------------------

    keywords = SPECIALTY_KEYWORDS.get(
        requested,
        [requested]
    )


    # -----------------------------------------------------
    # COMBINE AVAILABLE HOSPITAL INFORMATION
    # -----------------------------------------------------

    combined_text = (
        hospital_name
        + " "
        + hospital_specialty
    )


    # -----------------------------------------------------
    # EXACT / STRONG MATCH
    # -----------------------------------------------------

    for keyword in keywords:

        if keyword in combined_text:

            return 100


    # -----------------------------------------------------
    # NO MATCH
    # -----------------------------------------------------

    return 0


# =========================================================
# ACCESSIBILITY SCORE
# =========================================================

def calculate_accessibility_score(
    accessibility_score
):

    if accessibility_score is None:

        return 50

    try:

        score = float(
            accessibility_score
        )

        return round(
            max(
                0,
                min(100, score)
            ),
            2
        )

    except Exception:

        return 50


# =========================================================
# FINAL AI SCORE
# =========================================================

def calculate_ai_score(
    distance_score,
    specialty_score,
    accessibility_score,
    emergency_score,
    healthcare_type_score
):

    """
    Weighted recommendation score.

    Current proposed weights:

    Distance       = 30%
    Specialty      = 25%
    Accessibility  = 25%
    Emergency      = 10%
    Healthcare     = 10%
    """

    score = (

        distance_score * 0.30

        +

        specialty_score * 0.25

        +

        accessibility_score * 0.25

        +

        emergency_score * 0.10

        +

        healthcare_type_score * 0.10
    )

    return round(
        score,
        2
    )


# =========================================================
# HOSPITAL RECOMMENDATION
# =========================================================

def recommend_hospitals(
    patient_lat,
    patient_lon,
    requested_specialty=None,
    top_n=5
):

    # -----------------------------------------------------
    # LOAD HOSPITAL DATA
    # -----------------------------------------------------

    hospitals = load_hospitals()

    # -----------------------------------------------------
    # LOAD REAL GIS ACCESSIBILITY SCORES
    # -----------------------------------------------------

    accessibility_lookup = (
        load_accessibility_scores()
    )

    results = []

    # -----------------------------------------------------
    # PROCESS EACH HOSPITAL
    # -----------------------------------------------------

    for _, hospital in hospitals.iterrows():

        try:

            hospital_lat = float(
                hospital["Latitude"]
            )

            hospital_lon = float(
                hospital["Longitude"]
            )

        except Exception:

            continue


        # -------------------------------------------------
        # HOSPITAL NAME
        # -------------------------------------------------

        hospital_name = hospital.get(
            "Hospital_Name",
            ""
        )

        if pd.isna(hospital_name):

            hospital_name = (
                f"Hospital "
                f"({hospital_lat:.5f}, "
                f"{hospital_lon:.5f})"
            )


        # -------------------------------------------------
        # DISTANCE
        # -------------------------------------------------

        distance_km = haversine_distance(
            patient_lat,
            patient_lon,
            hospital_lat,
            hospital_lon
        )

        distance_score = (
            calculate_distance_score(
                distance_km
            )
        )


        # -------------------------------------------------
        # SPECIALTY
        # -------------------------------------------------

        specialty_score = (
            calculate_specialty_match(
                hospital_name,
                hospital.get(
                    "Specialty",
                    ""
                ),
                requested_specialty
            )
        )


        # -------------------------------------------------
        # ACCESSIBILITY
        # -------------------------------------------------

        key = (
            round(hospital_lat, 6),
            round(hospital_lon, 6)
        )

        accessibility_value = (
            accessibility_lookup.get(
                key,
                None
            )
        )

        if accessibility_value is None:

            print(
                "WARNING: Accessibility score "
                "not found for:",
                hospital_name,
                hospital_lat,
                hospital_lon
            )

        accessibility_score = (
            calculate_accessibility_score(
                accessibility_value
            )
        )


        # -------------------------------------------------
        # EMERGENCY
        # -------------------------------------------------

        emergency_score = (
            calculate_emergency_score(
                hospital.get(
                    "Emergency",
                    ""
                )
            )
        )


        # -------------------------------------------------
        # HEALTHCARE TYPE
        # -------------------------------------------------

        healthcare_type_score = (
            calculate_healthcare_type_score(
                hospital.get(
                    "Healthcare_Type",
                    ""
                )
            )
        )


        # -------------------------------------------------
        # FINAL AI SCORE
        # -------------------------------------------------

        ai_score = calculate_ai_score(

            distance_score,

            specialty_score,

            accessibility_score,

            emergency_score,

            healthcare_type_score
        )


        # -------------------------------------------------
        # STORE RESULT
        # -------------------------------------------------

        results.append({

            "Hospital":
                hospital_name,

            "Latitude":
                hospital_lat,

            "Longitude":
                hospital_lon,

            "Distance (km)":
                round(
                    distance_km,
                    2
                ),

            "Distance Score":
                distance_score,

            "Accessibility Score":
                accessibility_score,

            "Specialty Match Score":
                specialty_score,

            "Emergency Score":
                emergency_score,

            "Healthcare Type Score":
                healthcare_type_score,

            "AI Score":
                ai_score
        })


    # =====================================================
    # CREATE DATAFRAME
    # =====================================================

    result_df = pd.DataFrame(
        results
    )


    if result_df.empty:

        return result_df


    # =====================================================
    # SORT
    # =====================================================

    result_df = result_df.sort_values(

        by=[
            "AI Score",
            "Distance (km)"
        ],

        ascending=[
            False,
            True
        ]
    )


    # =====================================================
    # TOP N
    # =====================================================

    result_df = result_df.head(
        top_n
    ).reset_index(
        drop=True
    )


    # =====================================================
    # RANK
    # =====================================================

    result_df.insert(
        0,
        "Rank",
        range(
            1,
            len(result_df) + 1
        )
    )


    return result_df