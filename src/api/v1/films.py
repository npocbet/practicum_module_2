from http import HTTPStatus
from pprint import pprint

from fastapi import APIRouter, Depends, Request, HTTPException
from models.film import AllShortFilms, Film, FilmShort
from models.paginators import PaginateModel
from models.query_filters import QueryFilterModel

from services.film import FilmService, get_film_service


router = APIRouter() # Объект router, в котором регистрируем обработчики

# https://pydantic-docs.helpmanual.io
# /api/v1/films?sort=-imdb_rating&page[limit]=50&page[offset]=1

# Внедряем FilmService с помощью Depends(get_film_service) 
@router.get('/{film_id}', response_model=Film) # Позже подключим роутер к корневому роутеру   /api/v1/film/some_id
async def film_details(film_id: str, film_service: FilmService = Depends(get_film_service)) -> Film: 
    # "get_persons_films_list-/api/v1/persons/046b28db-3db5-4ba8-8867-136b19624c7a/films-page[number]-1-page[size]-2-sort-id"
    redis_key = f"movies-get-film-/api/v1/films/{film_id}"
    film = await film_service.get_by_id(redis_key, film_id)
    if not film:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail='film not found')
    #return Film(id=film.id, title=film.title)
    #film.json()
    #print(film.id)
    return film #Film(id=film.id)


# http://127.0.0.1:8104/api/v1/films?filter[genre]=Comedy&page[size]=3&page[number]=6&sort=-imdb_rating&sort=created
#@router.get('/', response_model=AllFilms)
@router.get('/', response_model=AllShortFilms)
async def get_film_list(request: Request,
                        # sort: str = None,
                        filter_by: QueryFilterModel = Depends(QueryFilterModel),
                        pagination: PaginateModel = Depends(PaginateModel),
                        film_service: FilmService = Depends(get_film_service)
) -> AllShortFilms:
    # http://127.0.0.1:8105/api/v1/films/?filter[genre]=Comedy&page[size]=3&page[number]=6&sort=imdb_rating&sort=-created
    # output {"imdb_rating":"asc","created":"desc"}
    redis_key = f"movies-get-film-/api/v1/films/pnum:{pagination.page_number}-psize:{pagination.page_number}-filter:{filter_by.filter_by_genre}:{filter_by.filter_by_director}"
    film = await film_service.get_paginated_movies(redis_key,
                                      offset=pagination.offset,
                                      limit=pagination.page_size,
                                      filter_by=filter_by.get_filter_for_elastic())

    to_res = [FilmShort(**source['_source']) for source in film['hits']['hits']]
    amount = film['hits']['total']['value']
    responce = AllShortFilms(page_size=pagination.page_size, page_number=pagination.page_number, results=to_res, amount_results=amount)
    responce.json()
    return responce


# http://127.0.0.1:8104/api/v1/films/search/?query=Captain films 2. Поиск
@router.get('/search')
async def search_film_by_query(query: str = None,
                               sort: str = None,
                               filter_by: QueryFilterModel = Depends(QueryFilterModel),
                               pagination: PaginateModel = Depends(PaginateModel),
                               film_service: FilmService = Depends(get_film_service)
):
    #film = await film_service.get_items_by_query()
    all
    return {}

#python -m uvicorn main:app --port=8106 --reload
