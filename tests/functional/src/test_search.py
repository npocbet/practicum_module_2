import json
import aiohttp
from tests.functional.settings import test_settings_films, test_settings_genres, test_settings_persons
import pytest

#  Название теста должно начинаться со слова `test_`
#  Любой тест с асинхронными вызовами нужно оборачивать декоратором `pytest.mark.asyncio`, который следит за запуском и работой цикла событий.

@pytest.mark.asyncio
async def test_search_films(elasticsearch_client):
    # 1. Генерируем данные для ES
    settings = test_settings_films
    es_data = settings.es_data

    bulk_query = []
    for row in es_data:
        bulk_query.extend([
            # json.dumps({'index': {'_index': test_settings.es_index, '_id': row[test_settings.es_id_field]}}),
            json.dumps({'index': {'_index': settings.es_index,
                                  '_id': row[settings.es_id_field]}}),
            json.dumps(row)
        ])

    str_query = '\n'.join(bulk_query) + '\n'

    # 2. Загружаем данные в ES

    es_client = elasticsearch_client
    response = await es_client.bulk(str_query, refresh=True)
    if response['errors']:
        raise Exception('Ошибка записи данных в Elasticsearch', response)

    # 3. Запрашиваем данные из ES по API

    session = aiohttp.ClientSession()
    url = settings.service_url + settings.api_uri
    async with session.get(url, params=settings.query_data) as response:
        body = await response.json()
        # headers = response.headers
        status = response.status
    await session.close()

    # 4. Проверяем ответ
    assert status == 200
    assert len(body['results']) == 50


@pytest.mark.asyncio
async def test_search_persons(elasticsearch_client):
    # 1. Генерируем данные для ES
    settings = test_settings_persons
    es_data = settings.es_data

    bulk_query = []
    for row in es_data:
        bulk_query.extend([
            json.dumps({'index': {'_index': settings.es_index,
                                  '_id': row[settings.es_id_field]}}),
            json.dumps(row)
        ])

    str_query = '\n'.join(bulk_query) + '\n'

    # 2. Загружаем данные в ES

    es_client = elasticsearch_client
    response = await es_client.bulk(str_query, refresh=True)
    if response['errors']:
        raise Exception('Ошибка записи данных в Elasticsearch', response)

    # 3. Запрашиваем данные из ES по API

    session = aiohttp.ClientSession()
    url = settings.service_url + settings.api_uri
    async with session.get(url, params=settings.query_data) as response:
        body = await response.json()
        headers = response.headers
        status = response.status
    await session.close()

    # 4. Проверяем ответ
    assert status == 200
    assert len(body['results']) == 50
