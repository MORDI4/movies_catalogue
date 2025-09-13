import requests
import random
import os

BASE_DIR = os.path.dirname(__file__)
print(BASE_DIR)
with open(os.path.join(BASE_DIR, "API_key.txt"), "r") as f:
    API_TOKEN = f.read().strip()

API_URL = "https://api.themoviedb.org/3/"

name_list = ['top_rated', 'upcoming', 'popular', 'now_playing']


def call_tmdb_api(endpoint):
    """Wspólna funkcja do wykonywania zapytań do API TMDB."""
    full_url = f"{API_URL}{endpoint}"
    headers = {
        "Authorization": f"Bearer {API_TOKEN}"
    }
    response = requests.get(full_url, headers=headers)
    response.raise_for_status()
    return response.json()


def get_movies_list(list_type):
    data = call_tmdb_api(f"movie/{list_type}")
    return [
        {
            'id': movie['id'],
            'title': movie['title'],
            'poster_path': movie['poster_path']
        }
        for movie in data['results']
    ]


def get_movies(num, list_name='popular'):
    data = get_movies_list(list_name)
    random.shuffle(data)
    return data[:num]


def get_poster_url(path, size='w342'):
    return f'https://image.tmdb.org/t/p/{size}{path}'


def get_random_backdrop(movie_id):
    data = call_tmdb_api(f"movie/{movie_id}/images")
    return data['backdrops'][random.randint(0, len(data['backdrops']) - 1)]['file_path']


def get_movie_details(movie_id):
    response1 = call_tmdb_api(f"movie/{movie_id}")
    response2 = call_tmdb_api(f"movie/{movie_id}/credits")
    return {
        'title': response1['title'],
        'tagline': response1['tagline'],
        'overview': response1['overview'],
        'genres': response1['genres'],
        'budget': response1['budget'],
        'backdrop_path': get_random_backdrop(movie_id),
        'cast': [
            {'name': i['name'], 'profile_path': i['profile_path']}
            for i in response2['cast']
        ]
    }
