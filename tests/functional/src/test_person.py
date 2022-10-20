import json
import pytest

from tests.functional.settings import test_settings_persons, test_settings_films


@pytest.mark.asyncio
async def test_persons_id(elasticsearch_client, session_client):
    # 1. Генерируем данные для ES
    settings = test_settings_persons
    es_data = settings.es_data[-1]

    bulk_query = [
        json.dumps({'index': {'_index': settings.es_index,
                              '_id': es_data[settings.es_id_field]}}),
        json.dumps(es_data)
    ]

    str_query = '\n'.join(bulk_query) + '\n'

    # 2. Загружаем данные в ES

    response = await elasticsearch_client.bulk(str_query, refresh=True)
    if response['errors']:
        raise Exception('Ошибка записи данных в Elasticsearch', response)

    # 3. Запрашиваем данные из ES по API

    url = settings.service_url + settings.api_uri + '/' + str(es_data[settings.es_id_field])
    async with session_client.get(url, params=settings.query_data) as response:
        body = await response.json()
        status = response.status

    # 4. Проверяем ответ
    assert status == 200
    assert body['id'] == es_data[settings.es_id_field]


@pytest.mark.asyncio
async def test_persons_films_by_id(elasticsearch_client, session_client):
    # 1. Генерируем данные для ES
    p_settings = test_settings_persons
    p_es_data = p_settings.es_data[-2]
    f_settings = test_settings_films
    f_es_data = f_settings.es_data[-2]

    # добавим данные о сгенерированном актере к сгенерированному фильму
    f_es_data['actors_names'].append(p_es_data['full_name'])
    f_es_data['actors'].append({'id': p_es_data['id'], 'name': p_es_data['full_name']})
    bulk_query = [
        json.dumps({'index': {'_index': p_settings.es_index,
                              '_id': p_es_data[p_settings.es_id_field]}}),
        json.dumps(p_es_data),
        json.dumps({'index': {'_index': f_settings.es_index,
                              '_id': f_es_data[f_settings.es_id_field]}}),
        json.dumps(f_es_data)
    ]

    str_query = '\n'.join(bulk_query) + '\n'

    # 2. Загружаем данные в ES

    response = await elasticsearch_client.bulk(str_query, refresh=True)
    if response['errors']:
        raise Exception('Ошибка записи данных в Elasticsearch', response)

    # 3. Запрашиваем данные из ES по API

    url = p_settings.service_url + p_settings.api_uri + '/' + \
          str(p_es_data[p_settings.es_id_field]) + '/film/'
    async with session_client.get(url, params=p_settings.query_data) as response:
        body = await response.json()
        status = response.status

    # 4. Проверяем ответ
    assert status == 200
    assert f_es_data[p_settings.es_id_field] in (i['id'] for i in body['results'])
