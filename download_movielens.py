import os
import zipfile
import requests
from io import BytesIO

# URL officielle du dataset MovieLens 100k
url = "https://files.grouplens.org/datasets/movielens/ml-latest-small.zip"

# Dossier de destination
output_dir = "data/raw"
os.makedirs(output_dir, exist_ok=True)

# Télécharger l'archive ZIP
print("Téléchargement du dataset MovieLens...")
response = requests.get(url)
if response.status_code == 200:
    print("Téléchargement réussi. Extraction en cours...")

    # Extraire le ZIP en mémoire
    with zipfile.ZipFile(BytesIO(response.content)) as zip_file:
        for name in zip_file.namelist():
            if name.endswith(".csv"):
                zip_file.extract(name, output_dir)
                print(f"✔️ Fichier extrait : {name}")
    print("✅ Tous les fichiers CSV ont été extraits dans:", output_dir)
else:
    print("❌ Erreur lors du téléchargement :", response.status_code)
