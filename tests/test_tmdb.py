import tmdb_client
from unittest.mock import Mock

def test_get_poster_url_uses_default_size():
    # Przygotowanie danych
    poster_api_path = "some-poster-path"
    expected_default_size = 'w342'
    # Wywołanie kodu, który testujemy
    poster_url = tmdb_client.get_poster_url(poster_api_path)
    # Porównanie wyników
    assert expected_default_size in poster_url

def test_get_movies_list_type_popular():
    movies_list = tmdb_client.get_movies_list("popular")
    assert movies_list is not None

def test_get_movies_list(monkeypatch):
    # Lista, która będzie zwracać przysłonięte "zapytanie" do API
    mock_response_data = {
        "results": [
            {"id": 1, "title": "Movie 1", "poster_path": "/x.jpg"},
            {"id": 2, "title": "Movie 2", "poster_path": "/y.jpg"},
        ]
    }

    requests_mock = Mock()
    # Wynik wywołania zapytania do API
    response = requests_mock.return_value
    # Przysłaniamy wynik wywołania metody .json()
    response.json.return_value = mock_response_data
    monkeypatch.setattr("tmdb_client.requests.get", requests_mock)

    movie_list = tmdb_client.get_movies_list("popular")
    expected = [
        {"id": 1, "title": "Movie 1", "poster_path": "/x.jpg"},
        {"id": 2, "title": "Movie 2", "poster_path": "/y.jpg"},
    ]

    assert movie_list == expected


