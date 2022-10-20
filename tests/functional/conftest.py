import aiohttp
import aioredis
import pytest_asyncio
from elasticsearch import AsyncElasticsearch

from tests.functional.settings import test_settings


@pytest_asyncio.fixture(scope="function")
async def elasticsearch_client():
    es_client = AsyncElasticsearch(hosts=test_settings.es_host_url,
                                   validate_cert=False,
                                   use_ssl=False)

    yield es_client
    await es_client.close()


@pytest_asyncio.fixture(scope="function")
async def session_client():
    session = aiohttp.ClientSession()
    yield session
    await session.close()


# @pytest_asyncio.fixture(scope="function")
# async def redis_client():
#     redis = await aioredis.create_redis_pool(
#         (test_settings.redis_host, test_settings.redis_port), minsize=10, maxsize=20
#     )
#     yield redis
#     await redis.wait_closed()
