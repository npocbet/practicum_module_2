from pprint import pprint
from typing import Optional
from elasticsearch import AsyncElasticsearch

es: Optional[AsyncElasticsearch] = None
# docker run -d -p 9200:9200 --name flled_elastic_v2 filled_elastic_v1

# Функция понадобится при внедрении зависимостей
def get_elastic() -> AsyncElasticsearch:
    return es


async def get_movie_by_id(es_i, id: str):
    query_body = {
        "query": {
            "match": {
                "id": id
            }
        }
    }
    result = await es_i.search(index="movies", body=query_body)
    return result['hits']['hits']


async def get_movies(es_i, number_of_movies=10, filter=None, offset=0):
    if filter is None:
        query_body = {
            "query": {
                "match_all": {},
            },
            "sort": [{"imdb_rating": "desc"}],
        }
        result = await es_i.search(index="movies", body=query_body, from_=offset, size=number_of_movies)
        return result['hits']['hits']
    else:
        query_body = {
            "query": {
                "bool": {
                    "filter": {
                        "match": {
                            **filter
                        }
                    }
                }
            },
            "sort": [{"imdb_rating": "desc"}],
        }
        result = await es_i.search(index="movies", body=query_body, from_=offset, size=number_of_movies)
        result = [i['_source'] for i in result['hits']['hits']]
        return result

# docker run -d -p 9200:9200 --name flled_elastic_v2 filled_elastic_v1

# loop = asyncio.get_event_loop()
# # пример с фильтром и количеством, оба параметры - необязательные
# r = loop.run_until_complete(get_movies(get_elastic(), 15,
#                                        filter={'genre': 'Short'}, offset=5))
#
# pprint(r)
# pprint(len(r))