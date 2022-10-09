from pprint import pprint
from functools import lru_cache
from typing import Dict, Optional

from aioredis import Redis
from elasticsearch import AsyncElasticsearch, NotFoundError
from fastapi import Depends

from db.elastic import get_elastic
from db.redis import get_redis
from models.film import Film
from core.config import FILM_CACHE_EXPIRE_IN_SECONDS


class FilmService:
    def __init__(self, redis: Redis, elastic: AsyncElasticsearch):
        self.redis = redis
        self.elastic = elastic

    # get_by_id возвращает объект фильма. Он опционален, так как фильм может отсутствовать в базе
    async def get_by_id(self, redis_key: str, film_id: str) -> Optional[Film]:
        # Пытаемся получить данные из кеша, потому что оно работает быстрее
        #film = await self._film_from_cache(redis_key)
        film = None
        if not film:
            # Если фильма нет в кеше, то ищем его в Elasticsearch
            #film = await self._get_film_from_elastic(film_id)
            film = await self.get_movie_by_id(film_id)
            if not film:
                # Если он отсутствует в Elasticsearch, значит, фильма вообще нет в базе
                return None
            film.json()
            try:
                pprint(film.json())
            except Exception:
                pass
            print('\n\n\n\n')
            # Сохраняем фильм  в кеш
            #await self._put_result_to_cache(redis_key, film.json())
            #await self._put_result_to_cache(redis_key, film)
        return film


    async def get_paginated_movies(self, redis_key, offset=0, limit=10, filter_by=None, sort=None):
        #film = await self._film_from_cache(redis_key)
        film = None # ЗАГЛУШКА
        # film = await self._film_from_cache()
        print('eto filter from pag', filter_by)
        if film is None: 
            film = await self._get_movies_from_elastic(offset, limit, filter_by, sort)
            if film is None:
                return None
            #await self._put_result_to_cache(redis_key, film)
        return film

    async def get_movie_by_id(self, film_id: str):
        query_body = {
            "query": {
                "match": {
                    "id": film_id
                }
            }
        }
        result = await self.elastic.search(index="movies", body=query_body)
        try:
            film = Film(**result['hits']['hits'][0].get('_source'))
        except IndexError:
            return None
        pprint(Film(**result['hits']['hits'][0].get('_source')))
        #return Film(**result['hits']['hits'][0].get('_source'))
        return film

    async def _get_movies_from_elastic(self,
                                       offset: int = 0,
                                       limit: int = 10,
                                       filter_by: Dict = None,
                                       sort: Dict = None):

        if sort is None:
            sort = {"imdb_rating": "desc"}

        if filter_by is None:
            query_body = {
                "query": {
                    "match_all": {},
                },
                "sort": [sort],
            }
            result = await self.elastic.search(index="movies", body=query_body, from_=offset, size=limit)
            return result
        else:
            query_body = {
                "query": {
                    "bool": {
                        "filter": {
                            "match": {
                                **filter_by
                            }
                        }
                    }
                },
                "sort": [sort],
            }
            result = await self.elastic.search(index="movies", body=query_body, from_=offset, size=limit)

            return result


    async def _film_from_cache(self, redis_key: str) -> Optional[Film]:
        # Пытаемся получить данные о фильме из кеша, используя команду get
        # https://redis.io/commands/get
        data = await self.redis.get(redis_key)
        print('data:', data)
        if not data:
            return None

        # pydantic предоставляет удобное API для создания объекта моделей из json
        try:
            film = Film.parse_raw(data)
        except Exception:
            pass
        #finally:
            #film = Film.parse_obj(data)
        return film

    #async def _put_film_to_cache(self, film: Film):
    async def _put_result_to_cache(self, redis_key:str, film): # TODO Проверить модель Film
        # Сохраняем данные о фильме, используя команду set
        # Выставляем время жизни кеша — 5 минут
        # https://redis.io/commands/set
        # pydantic позволяет сериализовать модель в json
        #await self.redis.set(redis_key, film.json(), expire=5) # FILM_CACHE_EXPIRE_IN_SECONDS) # ORIGINAL
        await self.redis.set(redis_key, film, expire=FILM_CACHE_EXPIRE_IN_SECONDS)
# get_film_service — это провайдер FilmService. 
# С помощью Depends он сообщает, что ему необходимы Redis и Elasticsearch
# Для их получения вы ранее создали функции-провайдеры в модуле db
# Используем lru_cache-декоратор, чтобы создать объект сервиса в едином экземпляре (синглтона)
@lru_cache()
def get_film_service(
        redis: Redis = Depends(get_redis),
        elastic: AsyncElasticsearch = Depends(get_elastic),
) -> FilmService:
    return FilmService(redis, elastic)
