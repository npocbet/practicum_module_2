from aioredis import Redis
from elasticsearch import AsyncElasticsearch
from fastapi import Depends
from pydantic.tools import lru_cache

from db.elastic import get_elastic
from db.redis import get_redis
from models.film import Person


class PersonService:
    def __init__(self, redis: Redis, elastic: AsyncElasticsearch):
        self.redis = redis
        self.elastic = elastic

    async def _get_person_by_id(self, person_id: str):
        query_body = {
            "query": {
                "match": {
                    "id": person_id
                }
            }
        }
        result = await self.elastic.search(index="persons", body=query_body)
        try:
            person = Person(**result['hits']['hits'][0].get('_source'))
            print(person)
        except IndexError:
            return None
        return person

@lru_cache()
def get_persons_service(
        redis: Redis = Depends(get_redis),
        elastic: AsyncElasticsearch = Depends(get_elastic),
) -> PersonService:
    return PersonService(redis, elastic)