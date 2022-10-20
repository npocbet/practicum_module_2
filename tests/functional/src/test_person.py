import json
import pytest

from tests.functional.settings import test_settings_persons


@pytest.mark.asyncio
async def test_persons_id(elasticsearch_client, session_client):
    # 1. Генерируем данные для ES
    settings = test_settings_persons
    es_data = settings.es_data

    bulk_query = [
        json.dumps({'index': {'_index': settings.es_index,
                              '_id': es_data[-1][settings.es_id_field]}}),
        json.dumps(es_data[-1])
    ]

    str_query = '\n'.join(bulk_query) + '\n'

    # 2. Загружаем данные в ES

    response = await elasticsearch_client.bulk(str_query, refresh=True)
    if response['errors']:
        raise Exception('Ошибка записи данных в Elasticsearch', response)

    # 3. Запрашиваем данные из ES по API

    url = settings.service_url + settings.api_uri + '/' + str(es_data[-1][settings.es_id_field])
    async with session_client.get(url, params=settings.query_data) as response:
        body = await response.json()
        status = response.status

    # 4. Проверяем ответ
    assert status == 200
    assert body['id'] == es_data[-1][settings.es_id_field]
