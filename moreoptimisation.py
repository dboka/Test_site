import geopandas as gpd
import os
import gzip

# ====== Folder Path ======
input_folder = r"C:\Users\deniss.boka\QGIS APSTRADE\DATA-AUTOMATISATION-QGIS\industry_riks\geojson"

# ====== Settings ======
coordinate_precision = 6   # reduces text size, but keeps geometry identical up to 10 cm precision
fields_to_keep = ["name", "Name", "NAME", "type", "Type", "TYPE"]  # keep only meaningful fields

# ====== Start Processing ======
for file in os.listdir(input_folder):
    if not file.lower().endswith(".geojson"):
        continue

    input_path = os.path.join(input_folder, file)
    optimized_path = input_path.replace(".geojson", "_optimized.geojson")
    gz_path = optimized_path + ".gz"

    try:
        print(f"📦 Processing: {file}")

        # --- Load the GeoJSON ---
        gdf = gpd.read_file(input_path)

        # --- Keep only relevant columns (geometry + name/type) ---
        gdf = gdf[[c for c in gdf.columns if c in fields_to_keep or c == "geometry"]]

        # --- Round coordinates slightly to shrink file size ---
        gdf["geometry"] = gdf["geometry"].apply(
            lambda geom: geom if geom.is_empty else geom.round(coordinate_precision)
            if hasattr(geom, "round") else geom
        )

        # --- Save temporarily optimized GeoJSON ---
        gdf.to_file(optimized_path, driver="GeoJSON")

        # --- Compress to GZIP ---
        with open(optimized_path, "rb") as f_in:
            with gzip.open(gz_path, "wb", compresslevel=9) as f_out:
                f_out.writelines(f_in)

        # --- Remove both original and temporary file ---
        os.remove(input_path)
        os.remove(optimized_path)

        print(f"✅ Saved & compressed: {os.path.basename(gz_path)}")

    except Exception as e:
        print(f"❌ Error in {file}: {e}")

print("\n🎯 Done! All GeoJSON files minimized, converted to .gz, and originals removed.")
