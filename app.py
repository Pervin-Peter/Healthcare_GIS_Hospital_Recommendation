from flask import Flask, render_template, request, jsonify
import pandas as pd
from Backend.hospital_recommender import recommend_hospitals

# =========================================================
# CLEAN DATA FOR VALID JSON
# =========================================================

def clean_dataframe_for_json(df):

    records = df.to_dict(orient="records")

    clean_records = []

    for record in records:

        clean_record = {}

        for key, value in record.items():

            if pd.isna(value):

                clean_record[key] = None

            else:

                clean_record[key] = value

        clean_records.append(clean_record)

    return clean_records

from Backend.data_loader import (
    load_hospitals,
    load_busstops,
    load_clinics,
    load_pharmacy,
    load_railway,
    load_recommendations
)


app = Flask(__name__)


# =========================================================
# HOME PAGE
# =========================================================

@app.route("/")
def home():

    return render_template("index.html")


# =========================================================
# HOSPITALS
# =========================================================

@app.route("/hospitals")
def hospitals():

    try:

        df = load_hospitals()

        hospital_df = df[
            [
                "Hospital_Name",
                "Latitude",
                "Longitude"
            ]
        ].copy()

        # Replace NaN / NaT with None
        # so Flask returns valid JSON.
        hospital_df = hospital_df.astype(object).where(
            pd.notna(hospital_df),
            None
        )

        records = hospital_df.to_dict(
            orient="records"
        )

        print(
            "Hospitals loaded:",
            len(records)
        )

        return jsonify(records)

    except Exception as e:

        print(
            "Hospital Loading Error:",
            e
        )

        return jsonify({
            "error": str(e)
        }), 500


# =========================================================
# BUS STOPS
# =========================================================

@app.route("/busstops")
def busstops():

    try:

        df = load_busstops()

        records = clean_dataframe_for_json(df)

        print("Bus Stops Loaded:", len(records))

        return jsonify(records)

    except Exception as e:

        print("Bus Stop Error:", e)

        return jsonify({
            "error": str(e)
        }), 500


# =========================================================
# CLINICS
# =========================================================

@app.route("/clinics")
def clinics():

    try:

        df = load_clinics()

        records = clean_dataframe_for_json(df)

        print("Clinics Loaded:", len(records))

        return jsonify(records)

    except Exception as e:

        print("Clinic Error:", e)

        return jsonify({
            "error": str(e)
        }), 500


# =========================================================
# PHARMACIES
# =========================================================

@app.route("/pharmacy")
def pharmacy():

    try:

        df = load_pharmacy()

        records = clean_dataframe_for_json(df)

        print("Pharmacy Loaded:", len(records))

        return jsonify(records)

    except Exception as e:

        print("Pharmacy Error:", e)

        return jsonify({
            "error": str(e)
        }), 500


# =========================================================
# RAILWAY STATIONS
# =========================================================

@app.route("/railway")
def railway():

    try:

        df = load_railway()

        records = clean_dataframe_for_json(df)

        print("Railway Loaded:", len(records))

        return jsonify(records)

    except Exception as e:

        print("Railway Error:", e)

        return jsonify({
            "error": str(e)
        }), 500


# =========================================================
# RECOMMENDED HOSPITAL ZONES
# =========================================================

@app.route("/recommendations")
def recommendations():

    df = load_recommendations()

    return jsonify(
        df.to_dict(orient="records")
    )


# =========================================================
# HOSPITAL RECOMMENDATION
# =========================================================

@app.route("/recommend", methods=["POST"])
def recommend():

    try:

        data = request.get_json()

        latitude = float(data["latitude"])
        longitude = float(data["longitude"])

        specialty = data.get(
            "specialty",
            ""
        )

        print(
            "Selected Specialty:",
            specialty
        )

        recommendations = recommend_hospitals(
            latitude,
            longitude,
            requested_specialty=specialty
        )

        records = recommendations.to_dict(
            orient="records"
        )

        clean_records = []

        for record in records:

            clean_record = {}

            for key, value in record.items():

                if pd.isna(value):
                    clean_record[key] = None
                else:
                    clean_record[key] = value

            clean_records.append(clean_record)

        return jsonify(clean_records)

    except Exception as e:

        print(
            "Recommendation Error:",
            e
        )

        return jsonify({
            "error": str(e)
        }), 500


# =========================================================
# START APPLICATION
# =========================================================

if __name__ == "__main__":

    app.run(
        debug=True
    )