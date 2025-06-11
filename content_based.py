
import pandas as pd

def recommend_by_genre(movie_title, df_movies, n=5):
    if movie_title not in df_movies['title'].values:
        return []

    # Trouver le genre du film sélectionné
    genre = df_movies[df_movies['title'] == movie_title]['genres'].values[0]

    # Trouver d'autres films avec le même genre
    similar_movies = df_movies[df_movies['genres'] == genre]

    # Supprimer le film lui-même de la liste
    similar_movies = similar_movies[similar_movies['title'] != movie_title]

    return similar_movies['title'].head(n).tolist()
