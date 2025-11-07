import gzip
import shutil
import os

# ====== Norādi mapi, kur ir tavi .gz faili ======
folder = r"C:\Users\deniss.boka\QGIS APSTRADE\DATA-AUTOMATISATION-QGIS\industry_riks\geojson"

for filename in os.listdir(folder):
    if filename.lower().endswith(".geojson.gz"):
        gz_path = os.path.join(folder, filename)
        geojson_path = gz_path.replace(".geojson.gz", ".geojson")

        print(f"🧩 Atspiežu: {filename} → {os.path.basename(geojson_path)}")

        # Atver .gz un izveido .geojson
        with gzip.open(gz_path, "rb") as f_in:
            with open(geojson_path, "wb") as f_out:
                shutil.copyfileobj(f_in, f_out)

print("\n✅ Visi faili ir atspiesti atpakaļ uz .geojson!")
print("👉 Tagad tu vari pārbaudīt, ka tie strādā kartē.")