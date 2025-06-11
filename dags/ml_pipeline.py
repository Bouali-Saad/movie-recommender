from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime
import pandas as pd
import psycopg2
from sklearn.neighbors import NearestNeighbors

def fetch_data():
    conn = psycopg2.connect(
        host="postgres",
        dbname="airflow",
        user="airflow",
        password="airflow"
    )
    movies = pd.read_sql("SELECT * FROM movies", conn)
    ratings = pd.read_sql("SELECT * FROM ratings", conn)
    conn.close()

    movies.to_csv("/opt/airflow/dags/data/ml/movies.csv", index=False)
    ratings.to_csv("/opt/airflow/dags/data/ml/ratings.csv", index=False)
    print("✅ Données extraites et sauvegardées.")

def build_model():
    ratings = pd.read_csv("/opt/airflow/dags/data/ml/ratings.csv")
    movies = pd.read_csv("/opt/airflow/dags/data/ml/movies.csv")

    matrix = ratings.pivot_table(index='userid', columns='movieid', values='rating')
    matrix.fillna(0, inplace=True)

    model = NearestNeighbors(metric='cosine', algorithm='brute')
    model.fit(matrix.T)

    movie_id = 1
    movie_idx = list(matrix.columns).index(movie_id)
    distances, indices = model.kneighbors([matrix.T.iloc[movie_idx]], n_neighbors=6)
    recommended_ids = matrix.columns[indices.flatten()[1:]]
    recommendations = movies[movies['movieid'].isin(recommended_ids)]
    print("🎬 Recommandations :\n", recommendations[['movieid', 'title', 'genres']])

with DAG(
    dag_id="movie_ml_pipeline",
    start_date=datetime(2024, 1, 1),
    schedule_interval=None,
    catchup=False,
    tags=["ml", "recommendation"]
) as dag:

    t1 = PythonOperator(
        task_id="fetch_data_from_postgres",
        python_callable=fetch_data
    )

    t2 = PythonOperator(
        task_id="train_and_recommend",
        python_callable=build_model
    )

    t1 >> t2
