
import streamlit as st
import pandas as pd
from sklearn.neighbors import NearestNeighbors
from content_based import recommend_by_genre

# Titre
st.title("🎬 Movie Recommender App")

# Chargement des données
@st.cache_data
def load_data():
    movies = pd.read_csv("dags/data/ml/movies.csv")
    ratings = pd.read_csv("dags/data/ml/ratings.csv")
    return movies, ratings

movies, ratings = load_data()

# Interface de sélection du film
movie_titles = movies.set_index('movieid')['title'].to_dict()
selected_title = st.selectbox("🎞️ Sélectionnez un film :", movie_titles.values())

# Récupérer le movieId
movie_id = next(key for key, value in movie_titles.items() if value == selected_title)

# Choix du mode
mode = st.radio(
    "Méthode de recommandation :",
    ("Collaborative Filtering (notes des utilisateurs)", "Content-Based Filtering (même genre)")
)

# Bouton pour lancer la recommandation
if st.button("🔁 Recommander"):
    st.write(f"🎯 Film sélectionné : {selected_title} (ID {movie_id})")

    if mode == "Collaborative Filtering (notes des utilisateurs)":
        # Création de la matrice utilisateur-film
        matrix = ratings.pivot_table(index='userid', columns='movieid', values='rating')
        matrix.fillna(0, inplace=True)

        # Entraînement du modèle KNN
        model = NearestNeighbors(metric='cosine', algorithm='brute')
        model.fit(matrix.T)

        if movie_id not in matrix.columns:
            st.error("❌ Ce film n'est pas dans la matrice.")
        else:
            movie_idx = list(matrix.columns).index(movie_id)
            distances, indices = model.kneighbors([matrix.T.iloc[movie_idx]], n_neighbors=6)
            recommended_ids = matrix.columns[indices.flatten()[1:]]
            recommendations = movies[movies['movieid'].isin(recommended_ids)]

            st.success("🎬 Voici les films recommandés :")
            st.dataframe(recommendations[['movieid', 'title', 'genres']].reset_index(drop=True))

    else:
        genre_recs = recommend_by_genre(selected_title, movies)
        if genre_recs:
            st.success("🎭 Films du même genre :")
            for movie in genre_recs:
                st.write(f"🎬 {movie}")
        else:
            st.write("Aucune recommandation trouvée pour ce genre.")
