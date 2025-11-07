import geopandas as gpd
import os

# ====== IEVADES CEĻI ======
blue_path = r"C:\Users\deniss.boka\Desktop\Boka_datuparbaude\KEM_upload_DParbaude_Boka\Kristapa paņēmiens EPSG 3857\Saule\Saule Red Slānis\Optimized_Joined_GPKG\joined_geopackage_joined.gpkg"
orange_path = r"C:\Users\deniss.boka\Desktop\Boka_datuparbaude\KEM_upload_DParbaude_Boka\Kristapa paņēmiens EPSG 3857\Saule\Saule oranzs Slānis\Optimized_Joined_GPKG\joined_geopackage_joined.gpkg"
yellow_path = r"C:\Users\deniss.boka\Desktop\Boka_datuparbaude\KEM_upload_DParbaude_Boka\Kristapa paņēmiens EPSG 3857\Saule\Saule dzeltens Slānis\Optimized_Joined_GPKG\joined_geopackage_joined.gpkg"

# ====== IZVADES MAPES CEĻŠ ======
output_folder = r"C:\Users\deniss.boka\Desktop\Boka_datuparbaude\KEM_upload_DParbaude_Boka\Kristapa paņēmiens EPSG 3857\Saule\Differenece Slani"
os.makedirs(output_folder, exist_ok=True)

orange_clean_path = os.path.join(output_folder, "orange_clean.gpkg")
yellow_clean_path = os.path.join(output_folder, "yellow_clean.gpkg")

print("📥 Loading layers...")
blue = gpd.read_file(blue_path)
orange = gpd.read_file(orange_path)
yellow = gpd.read_file(yellow_path)

# (1) — ORANŽAIS = ORANŽAIS - ZILAIS
print("🟠 Calculating orange minus blue...")
orange_clean = orange.overlay(blue, how="difference", keep_geom_type=True)
orange_clean.to_file(orange_clean_path, driver="GPKG")
print("✅ Orange clean layer saved:", orange_clean_path)

# (2) — DZELTENAIS = DZELTENAIS - (ZILAIS ∪ ORANŽAIS)
print("🟡 Calculating yellow minus (blue + orange)...")
blue_orange_union = gpd.overlay(blue, orange, how="union", keep_geom_type=True)
yellow_clean = yellow.overlay(blue_orange_union, how="difference", keep_geom_type=True)
yellow_clean.to_file(yellow_clean_path, driver="GPKG")
print("✅ Yellow clean layer saved:", yellow_clean_path)
