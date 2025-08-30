import requests
import random


url = 'https://api.themoviedb.org/3/movie/popular'

params = {
    "api_key": '9bc6d3d51e3b68e16c55d55a019c262d'
}

global results

def get_popular_movies():
    response = requests.get(url, params=params)
    return response.json()

def get_movies(num):
    data = get_popular_movies()
    random.shuffle(data['results'])
    return data['results'][:num]

results = get_movies(8)

def get_poster_url(path,size):
    return f'https://image.tmdb.org/t/p/{size}{path}'

def get_movie_info():
    movies_info = []
    for i in range(len(results)):
        movies_info.append({'title': results[i]['title'], 'poster_path': results[i]['poster_path']})
    return movies_info


