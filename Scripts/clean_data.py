import pandas as pd
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

INPUT_DIR = BASE_DIR / "Data" / "Final"
OUTPUT_DIR = BASE_DIR / "Data" / "Cleaned"

OUTPUT_DIR.mkdir(exist_ok=True)

FILES = [
    "Hospital_Master_Final.csv",
    "BusStops_Not_Covered.csv",
    "Clinics_Not_Covered.csv",
    "Pharmacy_Not_Covered.csv",
    "RailwayStations_Not_Covered.csv"
]

print("="*70)
print("GIS DATA QUALITY VALIDATION")
print("="*70)

for file in FILES:

    path = INPUT_DIR / file

    if not path.exists():
        continue

    print("\n"+"="*70)
    print(file)
    print("="*70)

    df = pd.read_csv(path)

    original = len(df)

    duplicate_rows = df.duplicated().sum()
    df = df.drop_duplicates()

    empty_rows = df.isnull().all(axis=1).sum()
    df = df.dropna(how="all")

    for col in df.select_dtypes(include="str").columns:
        df[col] = df[col].str.strip()

    # -------------------------
    # Detect Latitude Column
    # -------------------------

    lat_col = None

    for c in df.columns:
        if "lat" in c.lower():
            lat_col = c
            break

    # -------------------------
    # Detect Longitude Column
    # -------------------------

    lon_col = None

    for c in df.columns:
        if "lon" in c.lower():
            lon_col = c
            break

    missing_lat = 0
    missing_lon = 0
    invalid_lat = 0
    invalid_lon = 0

    if lat_col:

        missing_lat = df[lat_col].isna().sum()

        invalid_lat = (
            (df[lat_col] < -90) |
            (df[lat_col] > 90)
        ).sum()

    if lon_col:

        missing_lon = df[lon_col].isna().sum()

        invalid_lon = (
            (df[lon_col] < -180) |
            (df[lon_col] > 180)
        ).sum()

    duplicate_location = 0

    if lat_col and lon_col:

        duplicate_location = df.duplicated(
            subset=[lat_col, lon_col]
        ).sum()

    output = OUTPUT_DIR / file.replace(".csv","_Cleaned.csv")

    df.to_csv(output,index=False)

    print(f"Original Records      : {original}")
    print(f"Duplicate Rows        : {duplicate_rows}")
    print(f"Empty Rows            : {empty_rows}")
    print(f"Missing Latitude      : {missing_lat}")
    print(f"Missing Longitude     : {missing_lon}")
    print(f"Invalid Latitude      : {invalid_lat}")
    print(f"Invalid Longitude     : {invalid_lon}")
    print(f"Duplicate Coordinates : {duplicate_location}")
    print(f"Final Records         : {len(df)}")

print("\n")
print("="*70)
print("ALL DATASETS VALIDATED SUCCESSFULLY")
print("="*70)