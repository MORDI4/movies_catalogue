import requests
import random


url = 'https://api.themoviedb.org/3/movie/'

params = {
    "api_key": '9bc6d3d51e3b68e16c55d55a019c262d'
}

global results

def get_popular_movies():
    response = requests.get(f'{url}popular', params=params)
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
        movies_info.append({'id': results[i]['id'],'title': results[i]['title'], 'poster_path': results[i]['poster_path']})
    return movies_info

def get_movie_details(movie_id):
    response1 = requests.get(f'{url}{movie_id}', params=params).json()
    response2 = requests.get(f'{url}{movie_id}/credits', params=params).json()
    return {
        'title': response1['title'], 
        'tagline': response1['tagline'], 
        'overview': response1['overview'], 
        'genres': response1['genres'], 
        'budget': response1['budget'], 
        'backdrop_path': response1['backdrop_path'],
        'cast': [{'name': i['name'], 'profile_path': i['profile_path']} for i in response2['cast']]
        }
    





