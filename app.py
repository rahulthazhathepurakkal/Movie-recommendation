import streamlit as st
import pickle
import pandas as pd
import requests


def add_bg_from_url():
    st.markdown(
         f"""
         <style>
         .stApp {{
             background-image: url("https://motionarray.imgix.net/preview-62221JhKdV18thV_0000.jpg");
             background-attachment: fixed;
             background-size: cover
         }}
         </style>
         """,
         unsafe_allow_html=True
     )

add_bg_from_url()

def display_movies(names,posters):
    col1, col2, col3,col4,col5 = st.columns(5)

    with col1:
        st.image(posters[0])
        st.text(names[0])
    with col2:
        st.image(posters[1])
        st.text(names[1])
    with col3:
        st.image(posters[2])
        st.text(names[2])
    with col4:
        st.image(posters[3])
        st.text(names[3])
    with col5:
        st.image(posters[4])
        st.text(names[4])

def fetch_poster(movie_id):
    response=requests.get('https://api.themoviedb.org/3/movie/{}?api_key=0265ecd7b95a09235c6d7117b3d3f216&language=en-US'.format(movie_id))
    data= response.json()
    return "https://image.tmdb.org/t/p/w500" + data['poster_path']

def recommend(movie):
    movie_index = movies[movies['title'] == movie].index[0]
    distances = similarity[movie_index]
    movies_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:6]

    recommmended_movies=[]
    recommended_movies_posters=[]
    for i in movies_list:
        movie_id=movies.iloc[i[0]].movie_id
        #fetch poster from API
        recommmended_movies.append(movies.iloc[i[0]].title)
        recommended_movies_posters.append(fetch_poster(movie_id))
    return recommmended_movies,recommended_movies_posters

movies_dict=pickle.load(open('movie_dict.pkl','rb'))
movies=pd.DataFrame(movies_dict)

similarity=pickle.load(open('similarity.pkl','rb'))

st.title('Movie recommendation system')
selected_movie_name = st.selectbox(
    'Search a Movie',
    movies['title'].values)
if st.button('RECOMMEND'):
    names,posters=recommend(selected_movie_name)
    display_movies(names,posters)


st.subheader('You May Like These Action Movies')

#Action movies


action_dict=pickle.load(open('action_dict.pkl','rb'))
action=pd.DataFrame(action_dict).sample(n=10)
action_movie_names=action['title'].values[:5]
action_movie_id=action['movie_id'].values[:5]
action_posters=[]
for i in action_movie_id:
    posters=fetch_poster(i)
    action_posters.append(posters)

display_movies(action_movie_names,action_posters)

#Romance

st.subheader('Best Romantic Movies')

romance_dict=pickle.load(open('romance_dict.pkl','rb'))
romance=pd.DataFrame(romance_dict).sample(n=10)
romance_movie_names=romance['title'].values[:5]
romance_movie_id=romance['movie_id'].values[:5]
romance_posters=[]
for i in romance_movie_id:
    posters=fetch_poster(i)
    romance_posters.append(posters)

display_movies(romance_movie_names,romance_posters)
