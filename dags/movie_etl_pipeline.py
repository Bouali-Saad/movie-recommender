from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime
import pandas as pd
import psycopg2
import os

def extract_data():
    filepath = '/opt/airflow/dags/data/raw/movies.csv'
    print(f"🔎 Lecture de : {filepath}")
    
    if not os.path.exists(filepath):
        raise FileNotFoundError(f"❌ Le fichier {filepath} est introuvable dans le conteneur Airflow.")
    
    df = pd.read_csv(filepath)

    # Nettoyage
    df.drop_duplicates(inplace=True)
    df['year'] = df['title'].str.extract(r'\((\d{4})\)', expand=False)
    df['title'] = df['title'].str.replace(r'\(\d{4}\)', '', regex=True).str.strip()
    df['genres'] = df['genres'].replace('no genres listed', None)
    df = df.dropna(subset=['title', 'genres'])

    output_path = '/opt/airflow/dags/data/cleaned_movies.csv'
    df.to_csv(output_path, index=False)
    print(f"✅ Données nettoyées sauvegardées dans : {output_path}")

def load_to_postgres():
    print("🔌 Connexion à PostgreSQL...")
    conn = psycopg2.connect(
        host="postgres",
        dbname="airflow",
        user="airflow",
        password="airflow"
    )
    cur = conn.cursor()

    cur.execute("""
        CREATE TABLE IF NOT EXISTS movies (
            movieId INT,
            title TEXT,
            genres TEXT,
            year TEXT
        );
    """)

    filepath = '/opt/airflow/dags/data/cleaned_movies.csv'
    print(f"📥 Lecture des données nettoyées depuis : {filepath}")
    df = pd.read_csv(filepath)

    rows = df[['movieId', 'title', 'genres', 'year']].values.tolist()
    cur.executemany(
        "INSERT INTO movies (movieId, title, genres, year) VALUES (%s, %s, %s, %s)",
        rows
    )

    conn.commit()
    cur.close()
    conn.close()
    print("✅ Données insérées dans la base PostgreSQL.")

# === Définition du DAG ===

with DAG(
    dag_id="movie_etl_pipeline",
    start_date=datetime(2024, 1, 1),
    schedule_interval=None,
    catchup=False,
    tags=["etl", "movies"]
) as dag:

    task_extract = PythonOperator(
        task_id="extract_data",
        python_callable=extract_data
    )

    task_load = PythonOperator(
        task_id="load_to_postgres",
        python_callable=load_to_postgres
    )

    task_extract >> task_load
