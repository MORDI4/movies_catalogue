import requests
import random
import os

BASE_DIR = os.path.dirname(__file__)
print(BASE_DIR)
with open(os.path.join(BASE_DIR, "API_key.txt"), "r") as f:
    api_key = f.read().strip()

url = 'https://api.themoviedb.org/3/movie/'

params = {
    "api_key": api_key
}

name_list = ['top_rated', 'upcoming', 'popular', 'now_playing']

def get_movies_list(list_name):
    response = requests.get(f'{url}{list_name}', params=params).json()
    data = response['results']
    movies_list = []
    for i in range(len(data)):
        movies_list.append({'id': data[i]['id'],'title': data[i]['title'], 'poster_path': data[i]['poster_path']})
    return movies_list

def get_movies(num, list_name='popular'):
    data = get_movies_list(list_name)
    random.shuffle(data)
    return data[:num]

def get_poster_url(path,size):
    return f'https://image.tmdb.org/t/p/{size}{path}'

def get_random_backdrop(movie_id):
    response = requests.get(f'{url}{movie_id}/images', params=params).json()
    return response['backdrops'][random.randint(0,len(response['backdrops'])-1)]['file_path']

def get_movie_details(movie_id):
    response1 = requests.get(f'{url}{movie_id}', params=params).json()
    response2 = requests.get(f'{url}{movie_id}/credits', params=params).json()
    return {
        'title': response1['title'], 
        'tagline': response1['tagline'], 
        'overview': response1['overview'], 
        'genres': response1['genres'], 
        'budget': response1['budget'], 
        'backdrop_path': get_random_backdrop(movie_id),
        'cast': [{'name': i['name'], 'profile_path': i['profile_path']} for i in response2['cast']]
        }
    





