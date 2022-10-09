from pprint import pprint
from functools import lru_cache
from typing import Dict, Optional

from aioredis import Redis
from elasticsearch import AsyncElasticsearch, NotFoundError
from fastapi import Depends

from db.elastic import get_elastic
from db.redis import get_redis
from models.film import Genre, GenrePopularFilms
from core.config import FILM_CACHE_EXPIRE_IN_SECONDS


class GenreService:
    def __init__(self, redis: Redis, elastic: AsyncElasticsearch):
        self.redis = redis
        self.elastic = elastic


    async def get_genres(self, redis_key):
        #genres = await self._film_from_cache(redis_key)
        genres = None # TODO ЗАГЛУШКА
        if genres is None: 
            genres = await self._get_genres_from_elastic(offset=0, limit=30, filter_by=None, sort=None)
            if genres is None:
                return None
            #await _put_genre_in_cache(redis_key, genres) # TODO ЗАГЛУШКА
        return genres

    async def _get_genres_from_elastic(self, offset=0, limit=30, filter_by=None, sort=None):
        # TODO дописать логику 
        if filter_by is None:
            query_body = {
                "query": {
                    "match_all": {},
                },
            }
            result = await self.elastic.search(index="genres", body=query_body, from_=offset, size=limit)
            return result

# Используем lru_cache-декоратор, чтобы создать объект сервиса в едином экземпляре (синглтона)
@lru_cache()
def get_genre_service(
        redis: Redis = Depends(get_redis),
        elastic: AsyncElasticsearch = Depends(get_elastic),
) -> GenreService:
    return GenreService(redis, elastic)
