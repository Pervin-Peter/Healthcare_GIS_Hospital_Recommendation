import geopandas as gpd

files = {
    "Bus Stops": r"D:\SRM\Sem-3\GIS\Healthcare_GIS_Project\Shapefiles\bus_stop\BusStops.shp",
    "Railway Stations": r"D:\SRM\Sem-3\GIS\Healthcare_GIS_Project\Shapefiles\RailwayStations\RailwayStations.shp",
    "Clinics": r"D:\SRM\Sem-3\GIS\Healthcare_GIS_Project\Shapefiles\clinic\clinic.shp",
    "Pharmacies": r"D:\SRM\Sem-3\GIS\Healthcare_GIS_Project\Shapefiles\pharmacy\pharmacy.shp"
}

for name, path in files.items():

    print("\n==============================")
    print(name)
    print("==============================")

    gdf = gpd.read_file(path)

    print("Records:", len(gdf))
    print("CRS:", gdf.crs)
    print("Geometry:", gdf.geometry.geom_type.unique())
    print("Columns:")
    print(list(gdf.columns))

    print("\nFirst 3 records:")
    print(gdf.head(3))