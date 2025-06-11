from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime
import pandas as pd
import psycopg2
import os

def extract_ratings():
    filepath = '/opt/airflow/dags/data/raw/ratings.csv'
    print(f"📥 Lecture de : {filepath}")

    if not os.path.exists(filepath):
        raise FileNotFoundError(f"❌ Le fichier {filepath} est introuvable dans le conteneur Airflow.")

    df = pd.read_csv(filepath)
    df.dropna(inplace=True)

    df.to_csv('/opt/airflow/dags/data/cleaned_ratings.csv', index=False)
    print("✅ Données ratings nettoyées et sauvegardées.")

def load_ratings_to_postgres():
    print("🔌 Connexion à PostgreSQL pour les ratings...")
    conn = psycopg2.connect(
        host="postgres",
        dbname="airflow",
        user="airflow",
        password="airflow"
    )
    cur = conn.cursor()

    cur.execute("""
        CREATE TABLE IF NOT EXISTS ratings (
            userId INT,
            movieId INT,
            rating FLOAT,
            timestamp BIGINT
        );
    """)

    df = pd.read_csv('/opt/airflow/dags/data/cleaned_ratings.csv')

    rows = df[['userId', 'movieId', 'rating', 'timestamp']].values.tolist()
    cur.executemany(
        "INSERT INTO ratings (userId, movieId, rating, timestamp) VALUES (%s, %s, %s, %s)",
        rows
    )

    conn.commit()
    cur.close()
    conn.close()
    print("✅ Ratings insérées dans la base PostgreSQL.")

with DAG(
    dag_id="ratings_etl_pipeline",
    start_date=datetime(2024, 1, 1),
    schedule_interval=None,
    catchup=False,
    tags=["etl", "ratings"]
) as dag:

    task_extract_ratings = PythonOperator(
        task_id="extract_ratings",
        python_callable=extract_ratings
    )

    task_load_ratings = PythonOperator(
        task_id="load_ratings_to_postgres",
        python_callable=load_ratings_to_postgres
    )

    task_extract_ratings >> task_load_ratings
