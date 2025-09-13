import tmdb_client
from unittest.mock import Mock

# Mockowane dane
mock_movies = [
    {"id": 1, "title": "Movie 1", "poster_path": "/x.jpg"},
    {"id": 2, "title": "Movie 2", "poster_path": "/y.jpg"},
]

mock_results = {
    "results": mock_movies
}

mock_backdrops = {
    'backdrops': [
        {'file_path': 'some-path1'},
        {'file_path': 'some-path2'}
    ]
}

mock_movie = {
    "title": "Test Movie",
    "tagline": "The best movie",
    "overview": "Something happens",
    "genres": ["Action", "Drama"],
    "budget": 1000000,
}

mock_credits = {
    "cast": [
        {"name": "Actor 1", "profile_path": "/actor1.jpg"},
        {"name": "Actor 2", "profile_path": "/actor2.jpg"},
    ]
}

# ---------- TESTY ----------

def test_get_movies_list_returns_movies(monkeypatch):
    mock_call = Mock(return_value=mock_results)
    monkeypatch.setattr("tmdb_client.call_tmdb_api", mock_call)

    movie_list = tmdb_client.get_movies_list("popular")
    expected = [
        {"id": 1, "title": "Movie 1", "poster_path": "/x.jpg"},
        {"id": 2, "title": "Movie 2", "poster_path": "/y.jpg"},
    ]

    assert movie_list == expected


def test_get_movies_calls_correct_endpoint(monkeypatch):
    mock_call = Mock(return_value={"results": []})
    monkeypatch.setattr("tmdb_client.call_tmdb_api", mock_call)

    tmdb_client.get_movies_list("popular")

    mock_call.assert_called_once_with("movie/popular")


def test_get_movies_contains_expected_keys(monkeypatch):
    mock_call = Mock(return_value=mock_results)
    monkeypatch.setattr("tmdb_client.call_tmdb_api", mock_call)

    result = tmdb_client.get_movies_list("popular")

    for movie in result:
        assert set(movie.keys()) == {'id', 'title', 'poster_path'}


def test_get_movies_returns_movies(monkeypatch):
    mock_call = Mock(return_value=mock_movies)
    monkeypatch.setattr("tmdb_client.get_movies_list", mock_call)

    result = tmdb_client.get_movies(2)

    for movie in result:
        assert movie in mock_movies


def test_get_movies_correct_number(monkeypatch):
    mock_call = Mock(return_value=mock_movies)
    monkeypatch.setattr("tmdb_client.get_movies_list", mock_call)

    result = tmdb_client.get_movies(2)

    assert len(result) == 2


def test_get_poster_url_default_size():
    poster_api_path = '/some-path'
    expected_default_size = 'w342'

    poster_url = tmdb_client.get_poster_url(poster_api_path)

    assert expected_default_size in poster_url


def test_get_poster_url_returns_correct_url():
    poster_api_path = '/some-path'

    poster_url = tmdb_client.get_poster_url(poster_api_path)

    assert poster_url == f'https://image.tmdb.org/t/p/w342{poster_api_path}'


def test_get_random_backdrop_calls_correct_endpoint(monkeypatch):
    mock_call = Mock(return_value=mock_backdrops)
    monkeypatch.setattr("tmdb_client.call_tmdb_api", mock_call)

    tmdb_client.get_random_backdrop(2)

    mock_call.assert_called_once_with('movie/2/images')


def test_get_random_backdrop_returns_correct_url(monkeypatch):
    mock_call = Mock(return_value=mock_backdrops)
    monkeypatch.setattr("tmdb_client.call_tmdb_api", mock_call)

    result = tmdb_client.get_random_backdrop(2)

    file_paths = [d['file_path'] for d in mock_backdrops["backdrops"]]
    assert result in file_paths


def test_get_movie_details_calls_correct_endpoints(monkeypatch):
    mock_call = Mock(side_effect=[mock_movie, mock_credits])
    monkeypatch.setattr("tmdb_client.call_tmdb_api", mock_call)
    monkeypatch.setattr("tmdb_client.get_random_backdrop", Mock(return_value="some-path"))

    tmdb_client.get_movie_details(123)

    mock_call.assert_any_call("movie/123")
    mock_call.assert_any_call("movie/123/credits")


def test_get_movie_details_returns_correct_details(monkeypatch):
    mock_call = Mock(side_effect=[mock_movie, mock_credits])
    monkeypatch.setattr("tmdb_client.call_tmdb_api", mock_call)
    monkeypatch.setattr("tmdb_client.get_random_backdrop", Mock(return_value="some-path"))

    details = tmdb_client.get_movie_details(123)

    assert details["title"] == "Test Movie"
    assert details["tagline"] == "The best movie"
    assert details["budget"] == 1000000
    assert details["backdrop_path"] == "some-path"
    assert details["cast"][0]["name"] == "Actor 1"
