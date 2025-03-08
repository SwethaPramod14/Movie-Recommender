import streamlit as st
import pickle
import pandas as pd
import requests


def fetch_poster(movie_id):
        response = requests.get(
            'https://api.themoviedb.org/3/movie/{}?api_key=da4df99fa57950ca5b421bca58df9d4b&language=en-US'.format(
                movie_id))
        data = response.json()
        return "https://image.tmdb.org/t/p/w500/" + data['poster_path']

def recommend(movie):
    movie_index = movies[movies['title'] == movie].index[0]
    distances = similarity[movie_index]
    movies_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:6]

    recommended_movies = []
    recommended_movies_posters = []

    for i in movies_list:
        movie_id = movies.iloc[i[0]].movie_id

        recommended_movies.append(movies.iloc[i[0]].title)
        # fetch poster from api
        recommended_movies_posters.append(fetch_poster(movie_id))
    return recommended_movies, recommended_movies_posters


movies_dict =pickle.load(open('movie_dict.pkl','rb'))
movies = pd.DataFrame(movies_dict)

similarity = pickle.load(open('similarity.pkl','rb'))

# Add a background image slideshow using CSS
page_bg_img = '''
<style>
@keyframes slideshow {
    0% { background-image: url("https://i.postimg.cc/nhccLxbQ/Screenshot-2025-03-07-at-10-49-50-PM.png"); }
    33% { background-image: url("https://i.postimg.cc/L6C6nskF/Screenshot-2025-03-07-at-11-20-42-PM.png"); }
    66% { background-image: url("https://i.postimg.cc/FRn0TpyT/Screenshot-2025-03-07-at-11-00-08-PM.png"); }
    100% { background-image: url("https://i.postimg.cc/CxTp672v/Screenshot-2025-03-07-at-11-03-53-PM.png"); }
}

.stApp {
    animation: slideshow 30s infinite;
    background-size: cover;
    background-position: center;
    background-repeat: no-repeat;
    background-attachment: fixed;
}
</style>
'''
st.markdown(page_bg_img, unsafe_allow_html=True)

st.title("🎬 Movie Recommender System")
st.markdown("#### Find movies similar to your favorites!")
selected_movies_name = st.selectbox(
    'Search for movies:',
movies['title'].values)

if st.button('Recommend'):
    names, posters = recommend(selected_movies_name)
else:
    names, posters = [], []

coll, col2, col3, col4, col5 = st.columns(5)

if names and posters:
    with coll:
        st.text(names[0])
        st.image(posters[0])
    with col2:
        st.text(names[1])
        st.image(posters[1])
    with col3:
        st.text(names[2])
        st.image(posters[2])
    with col4:
        st.text(names[3])
        st.image(posters[3])
    with col5:
        st.text(names[4])
        st.image(posters[4])
