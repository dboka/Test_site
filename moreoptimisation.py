import geopandas as gpd
import os
import gzip
import shutil
import json

# =====================================================
# 📂 CONFIGURATION
# =====================================================
input_folder = r"C:\Users\deniss.boka\QGIS APSTRADE\DATA-AUTOMATISATION-QGIS\industry_riks\geojson"
simplify_tolerance = 0.00002    # visually safe simplification
decimal_precision = 6           # 6 decimals ≈ 10 cm precision
preserve_topology = True

# =====================================================
# ⚙️ GZIP FUNCTION
# =====================================================
def gzip_file(src_path, dst_path):
    with open(src_path, 'rb') as f_in:
        with gzip.open(dst_path, 'wb', compresslevel=9) as f_out:
            shutil.copyfileobj(f_in, f_out)

# =====================================================
# 🧩 RECURSIVE COORDINATE ROUNDER
# =====================================================
def round_coords(coords):
    if isinstance(coords, (float, int)):
        return round(coords, decimal_precision)
    if isinstance(coords, (list, tuple)):
        return [round_coords(c) for c in coords]
    return coords

# =====================================================
# 🚀 PROCESS ALL GEOJSON FILES
# =====================================================
for file in os.listdir(input_folder):
    if file.lower().endswith(".geojson"):
        path = os.path.join(input_folder, file)
        print(f"📥 Processing: {file}")

        try:
            # Load GeoJSON
            gdf = gpd.read_file(path)

            # Simplify (no visible geometry loss)
            gdf["geometry"] = gdf["geometry"].simplify(
                tolerance=simplify_tolerance,
                preserve_topology=preserve_topology
            )

            # Fix: convert datetime/Timestamp fields → string
            for col in gdf.columns:
                if gdf[col].dtype.name.startswith("datetime") or "Timestamp" in str(gdf[col].dtype):
                    gdf[col] = gdf[col].astype(str)

            # Convert GeoDataFrame → JSON dict
            tmp_json = json.loads(gdf.to_json())

            # Round geometry coordinates
            for feat in tmp_json["features"]:
                geom = feat.get("geometry")
                if geom and "coordinates" in geom:
                    geom["coordinates"] = round_coords(geom["coordinates"])

            # Write optimized GeoJSON (overwrite)
            with open(path, "w", encoding="utf-8") as f:
                json.dump(tmp_json, f, ensure_ascii=False)

            # Compress with gzip
            gz_path = path + ".gz"
            gzip_file(path, gz_path)

            orig_size = os.path.getsize(path) / 1024
            gz_size = os.path.getsize(gz_path) / 1024
            print(f"✅ {file}: {orig_size:.1f} KB → {gz_size:.1f} KB (GZ compressed)\n")

        except Exception as e:
            print(f"❌ Error processing {file}: {e}\n")

print("🎯 All GeoJSONs optimized and gzipped successfully!")


