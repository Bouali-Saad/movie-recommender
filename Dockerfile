
# Utiliser une image officielle de Python comme image de base
FROM python:3.10-slim

# Définir le répertoire de travail dans le conteneur
WORKDIR /app

# Copier les fichiers requirements.txt et le code de l'application
COPY requirements.txt requirements.txt
COPY recommender_app.py recommender_app.py
COPY dags/data/ml dags/data/ml
COPY content_based.py content_based.py

# Installer les dépendances
RUN pip install --no-cache-dir -r requirements.txt

# Exposer le port utilisé par Streamlit
EXPOSE 8501

# Commande pour lancer l'application Streamlit
CMD ["streamlit", "run", "recommender_app.py", "--server.port=8501", "--server.address=0.0.0.0"]
