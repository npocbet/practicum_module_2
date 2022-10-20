import json
import pytest
from tests.functional.settings import test_settings_films, test_settings_persons



#  Название теста должно начинаться со слова `test_`
#  Любой тест с асинхронными вызовами нужно оборачивать декоратором `pytest.mark.asyncio`, который следит за запуском и работой цикла событий.

@pytest.mark.asyncio
async def test_search_films(elasticsearch_client, session_client):
    # 1. Генерируем данные для ES
    settings = test_settings_films
    es_data = settings.es_data

    bulk_query = []
    for row in es_data[:50]:
        bulk_query.extend([
            json.dumps({'index': {'_index': settings.es_index,
                                  '_id': row[settings.es_id_field]}}),
            json.dumps(row)
        ])

    str_query = '\n'.join(bulk_query) + '\n'

    # 2. Загружаем данные в ES

    response = await elasticsearch_client.bulk(str_query, refresh=True)
    if response['errors']:
        raise Exception('Ошибка записи данных в Elasticsearch', response)

    # 3. Запрашиваем данные из ES по API

    url = settings.service_url + settings.api_uri + '/search/'
    async with session_client.get(url, params=settings.query_data) as response:
        body = await response.json()
        status = response.status

    # 4. Проверяем ответ
    assert status == 200
    assert len(body['results']) == 50


@pytest.mark.asyncio
async def test_search_persons(elasticsearch_client, session_client):
    # 1. Генерируем данные для ES
    settings = test_settings_persons
    es_data = settings.es_data

    bulk_query = []
    for row in es_data[:50]:
        bulk_query.extend([
            json.dumps({'index': {'_index': settings.es_index,
                                  '_id': row[settings.es_id_field]}}),
            json.dumps(row)
        ])

    str_query = '\n'.join(bulk_query) + '\n'

    # 2. Загружаем данные в ES

    response = await elasticsearch_client.bulk(str_query, refresh=True)
    if response['errors']:
        raise Exception('Ошибка записи данных в Elasticsearch', response)

    # 3. Запрашиваем данные из ES по API

    url = settings.service_url + settings.api_uri + '/search/'
    async with session_client.get(url, params=settings.query_data) as response:
        body = await response.json()
        status = response.status

    # 4. Проверяем ответ
    assert status == 200
    assert len(body['results']) == 50
