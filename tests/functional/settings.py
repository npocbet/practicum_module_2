import uuid

from pydantic import BaseSettings, Field


class TestSettings(BaseSettings):
    es_host: str = Field('http://127.0.0.1:9200', env='ELASTIC_HOST')
    redis_host: str = Field('http://127.0.0.1:6379', env='REDIS_HOST')
    service_url: str = Field('http://127.0.0.1:8106', env='SERVICE_HOST')


class TestSettingsFilms(TestSettings):
    es_index: str = 'movies'
    es_id_field: str = 'id'
    es_data = [{
        'id': str(uuid.uuid4()),
        'imdb_rating': 8.5,
        'genre': ['Action', 'Sci-Fi'],
        'title': 'Baaaazzzzziiiinga',
        'description': 'New World',
        'director': ['Stan'],
        'actors_names': ['Ann', 'Bob'],
        'writers_names': ['Ben', 'Howard'],
        'actors': [
            {'id': '111', 'name': 'Ann'},
            {'id': '222', 'name': 'Bob'}
        ],
        'writers': [
            {'id': '333', 'name': 'Ben'},
            {'id': '444', 'name': 'Howard'}
        ],
    } for _ in range(60)]
    api_uri = '/api/v1/films/search/'
    query_data = {'query': 'Baaaazzzzziiiinga'}


class TestSettingsPersons(TestSettings):
    es_index: str = 'persons'
    es_id_field: str = 'id'
    es_data = [{
        'id': str(uuid.uuid4()),
        'full_name': 'Lysiy iz brazzers',
    } for _ in range(60)]
    api_uri = '/api/v1/persons/search/'
    query_data = {'query': 'Lysiy iz brazzers'}


class TestSettingsGenres(TestSettings):
    es_index: str = 'genres'
    es_id_field: str = 'id'


test_settings = TestSettings()
test_settings_films = TestSettingsFilms()
test_settings_persons = TestSettingsPersons()
test_settings_genres = TestSettingsGenres()
