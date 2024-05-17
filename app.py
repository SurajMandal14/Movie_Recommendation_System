import streamlit as st
import pickle
import pandas as pd
import requests

# Function to fetch the poster of the movie
def fetch_poster(movie_id):
    response = requests.get(
        'https://api.themoviedb.org/3/movie/{}?api_key=8265bd1679663a7ea12ac168da84d2e8&language=en-US'.format(movie_id))
    data = response.json()
    return "https://image.tmdb.org/t/p/w500/" + data['poster_path']

# Load movie data and similarity matrix
movies_dict = pickle.load(open('movie_dict.pkl', 'rb'))
movies = pd.DataFrame(movies_dict)
similarity = pickle.load(open('similarity.pkl', 'rb'))

# Function to recommend movies
def recommend(movie):
    movie_index = movies[movies['title'] == movie].index[0]
    distances = similarity[movie_index]
    movies_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:6]
    recommended_movies = []
    recommended_movies_posters = []
    for i in movies_list:
        movie_id = movies.iloc[i[0]].movie_id
        recommended_movies.append(movies.iloc[i[0]].title)
        recommended_movies_posters.append(fetch_poster(movie_id))
    return recommended_movies, recommended_movies_posters

# Streamlit app title and author name
st.markdown("[View on GitHub](https://github.com/your-github-username/your-repo-name)", unsafe_allow_html=True)

st.title("MOVIE RECOMMENDATION SYSTEM")

st.markdown('<p style="color: black;">suraj kumar mandal dhanuk</p>', unsafe_allow_html=True)

# Selectbox for choosing a movie
selected_movie_name = st.selectbox('Select a movie:', movies['title'].values)

# Button for recommending movies
if st.button('Recommend'):
    names, posters = recommend(selected_movie_name)
    num_recommendations = min(5, len(names))
    for i in range(num_recommendations):
        st.text(names[i])
        st.image(posters[i])


