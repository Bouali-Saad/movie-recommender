
# 🎬 Movie Recommender System with Airflow, ML & Streamlit

A complete end-to-end movie recommendation system using collaborative and content-based filtering, orchestrated via Apache Airflow, and deployed as a web app with Streamlit + Docker.

---

## 🚀 Features

- ✅ Data extraction & cleaning using Apache Airflow
- 📊 Ratings & movie data processed and stored in PostgreSQL
- 🎯 Two recommendation engines:
  - **Collaborative Filtering** (user ratings with KNN)
  - **Content-Based Filtering** (movie genres)
- 🧪 Machine Learning integrated via Scikit-learn
- 🖥️ Streamlit web app for live recommendations
- 🐳 Dockerized for full portability

---

## 🗂️ Project Structure

```
movie_reco_project/
├── dags/
│   ├── data/
│   │   ├── raw/
│   │   └── ml/
│   ├── etl_movies_dag.py
│   ├── etl_ratings_dag.py
│   └── ml_pipeline_dag.py
├── content_based.py
├── recommender_app.py
├── requirements.txt
├── Dockerfile
```

---

## 🛠️ Setup Instructions

### 1. Clone & Build

```bash
git clone https://github.com/Bouali-Saad/movie_reco_project.git
cd movie_reco_project
docker build -t movie-recommender .
```

### 2. Run the App

```bash
docker run -p 8501:8501 movie-recommender
```

Visit 👉 [http://localhost:8501](http://localhost:8501)

---

## 📸 Screenshots
![image](https://github.com/user-attachments/assets/66197664-d666-4134-913e-e50b325a63ed)

![image](https://github.com/user-attachments/assets/6d00c059-1d85-4367-9a34-29006ba3c566)


![image](https://github.com/user-attachments/assets/8190c9a1-da74-41ae-af9c-10cfbb70abce)


---

## 👨‍💻 Author

**SAAD BOUALI**  
[LinkedIn Profile](https://www.linkedin.com/in/saad-bouali)  
Feel free to fork, star ⭐, or contribute!

---

## 📌 Tech Stack

- Apache Airflow
- PostgreSQL
- Scikit-learn
- Pandas
- Streamlit
- Docker
