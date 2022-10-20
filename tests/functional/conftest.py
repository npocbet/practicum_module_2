import pytest_asyncio
from elasticsearch import AsyncElasticsearch

from tests.functional.settings import test_settings


@pytest_asyncio.fixture(scope="function")
async def elasticsearch_client():
    elasticsearch_client = AsyncElasticsearch(hosts=test_settings.es_host,
                                              validate_cert=False,
                                              use_ssl=False)

    yield elasticsearch_client
    await elasticsearch_client.close()
