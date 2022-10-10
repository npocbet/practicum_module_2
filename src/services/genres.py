import db
from pprint import pp, pprint
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

    async def get_genre_by_id(self, redis_key, genre_id):
        genre = None # TODO ЗАГЛУШКА
        if genre is None: 
            genre = await self._get_genre_by_id_from_elastic(genre_id)
            if genre is None:
                return None
            #await _put_genre_in_cache(redis_key, genre) # TODO ЗАГЛУШКА
        return genre

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

    async def _get_genre_by_id_from_elastic(self, genre_id: str):
        query_body = {
            "query": {
                "match": {
                    "_id": genre_id
                }
            }
        }
        genre = await self.elastic.search(index="genres", body=query_body)
        return genre

# Используем lru_cache-декоратор, чтобы создать объект сервиса в едином экземпляре (синглтона)
@lru_cache()
def get_genre_service(
        redis: Redis = Depends(get_redis),
        elastic: AsyncElasticsearch = Depends(get_elastic),
) -> GenreService:
    return GenreService(redis, elastic)
