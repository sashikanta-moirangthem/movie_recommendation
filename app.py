import streamlit as st
import pickle
import pandas as pd
import requests

# TMDB API configuration
TMDB_API_KEY = "c0b8cdee5194a7169cec530d0a9a2618"
TMDB_BASE_URL = "https://api.themoviedb.org/3"

def fetch_poster(movie_id):
    response = requests.get(f"{TMDB_BASE_URL}/movie/{movie_id}?api_key={TMDB_API_KEY}&language=en-US")
    data = response.json()
    return f"https://image.tmdb.org/t/p/w500{data['poster_path']}"

def recommend(movie):
    movie_index = movies[movies['title'] == movie].index[0]
    distances = similarity[movie_index]
    movies_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[:6]  # Include top 6 instead of 5

    recommended_movies = []
    for i in movies_list:
        movie_id = movies.iloc[i[0]].movie_id
        recommended_movies.append({
            'title': movies.iloc[i[0]].title,
            'poster': fetch_poster(movie_id),
            'id': movie_id
        })
    return recommended_movies

# Load data
movies_dict = pickle.load(open('movie_dict.pkl', 'rb'))
movies = pd.DataFrame(movies_dict)
similarity = pickle.load(open('similarity.pkl', 'rb'))

# Streamlit UI
st.title('Movie Recommender System')

selected_movie_name = st.selectbox(
    'Enter the name of a movie you like, and we will recommend similar movies!',
    movies['title'].values
)

if st.button('Recommend'):
    recommendations = recommend(selected_movie_name)

    # Display selected movie
    st.subheader("Selected Movie:")
    col1, col2 = st.columns([1, 4])
    with col1:
        st.image(recommendations[0]['poster'], width=150)
    with col2:
        st.write(f"**{recommendations[0]['title']}**")
        tmdb_url = f"https://www.themoviedb.org/movie/{recommendations[0]['id']}"
        st.markdown(f"[View on TMDB]({tmdb_url})")

    # Display recommendations
    st.subheader("Recommendations:")
    cols = st.columns(5)
    for i, movie in enumerate(recommendations[1:], start=0):  # Start from index 1 to skip the selected movie
        with cols[i]:
            st.image(movie['poster'], use_column_width=True)
            tmdb_url = f"https://www.themoviedb.org/movie/{movie['id']}"
            st.markdown(f"[{movie['title']}]({tmdb_url})")

# CSS to improve the layout
st.markdown("""
    <style>
    .stSelectbox {
        margin-bottom: 20px;
    }
    .stButton {
        margin-bottom: 20px;
    }
    </style>
    """, unsafe_allow_html=True)