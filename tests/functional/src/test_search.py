import datetime
import uuid
import json

import aiohttp
import pytest

from elasticsearch import AsyncElasticsearch

from tests.functional.settings import test_settings


#  Название теста должно начинаться со слова `test_`
#  Любой тест с асинхронными вызовами нужно оборачивать декоратором `pytest.mark.asyncio`, который следит за запуском и работой цикла событий.

@pytest.mark.asyncio
async def test_search_films():
    # 1. Генерируем данные для ES

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
        # 'created_at': datetime.datetime.now().isoformat(),
        # 'updated_at': datetime.datetime.now().isoformat(),
        # 'film_work_type': 'movie'
    } for _ in range(60)]

    bulk_query = []
    for row in es_data:
        bulk_query.extend([
            # json.dumps({'index': {'_index': test_settings.es_index, '_id': row[test_settings.es_id_field]}}),
            json.dumps({'index': {'_index': 'movies', '_id': row['id']}}),
            json.dumps(row)
        ])

    str_query = '\n'.join(bulk_query) + '\n'

    # 2. Загружаем данные в ES

    es_client = AsyncElasticsearch(hosts=test_settings.es_host,
                                   validate_cert=False,
                                   use_ssl=False)
    response = await es_client.bulk(str_query, refresh=True)
    await es_client.close()
    if response['errors']:
        raise Exception('Ошибка записи данных в Elasticsearch', response)

    # 3. Запрашиваем данные из ES по API

    session = aiohttp.ClientSession()
    url = test_settings.service_url + '/api/v1/films/search/'
    # query_data = {'query':
    #                   {'match':
    #                        {'title': 'The Star'}
    #                    }
    #               }
    query_data = {'query': 'Baaaazzzzziiiinga'}
    async with session.get(url, params=query_data) as response:
        body = await response.json()
        headers = response.headers
        status = response.status
    await session.close()

    # 4. Проверяем ответ
    assert status == 200
    assert len(body['results']) == 50


@pytest.mark.asyncio
async def test_search_persons():
    # 1. Генерируем данные для ES

    es_data = [{
        'id': str(uuid.uuid4()),
        'full_name': 'Lysiy iz brazzers',
    } for _ in range(60)]

    bulk_query = []
    for row in es_data:
        bulk_query.extend([
            # json.dumps({'index': {'_index': test_settings.es_index, '_id': row[test_settings.es_id_field]}}),
            json.dumps({'index': {'_index': 'persons', '_id': row['id']}}),
            json.dumps(row)
        ])

    str_query = '\n'.join(bulk_query) + '\n'

    # 2. Загружаем данные в ES

    es_client = AsyncElasticsearch(hosts=test_settings.es_host,
                                   validate_cert=False,
                                   use_ssl=False)
    response = await es_client.bulk(str_query, refresh=True)
    await es_client.close()
    if response['errors']:
        raise Exception('Ошибка записи данных в Elasticsearch', response)

    # 3. Запрашиваем данные из ES по API

    session = aiohttp.ClientSession()
    url = test_settings.service_url + '/api/v1/persons/search/'
    query_data = {'query': 'Lysiy iz brazzers'}
    # query_data = {'query': 'Lysiy iz brazzers', 'pnum': 0, 'psize': 50}
    async with session.get(url, params=query_data) as response:
        body = await response.json()
        headers = response.headers
        status = response.status
    await session.close()

    # 4. Проверяем ответ
    assert status == 200
    assert len(body['results']) == 50
