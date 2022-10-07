from http import HTTPStatus

from fastapi import APIRouter, Depends, Request, HTTPException
from pydantic import BaseModel
from models.film import AllShortOutput, Film, AllFilms
from models.paginators import PaginateModel

from services.film import FilmService, get_film_service


router = APIRouter() # Объект router, в котором регистрируем обработчики

# Модель ответа API
# https://pydantic-docs.helpmanual.io
# У неё есть встроенные механизмы валидации, сериализации и десериализации
# class Film(BaseModel):
#     id: Any
#     title: str
# /api/v1/films?sort=-imdb_rating&page[limit]=50&page[offset]=1

# Внедряем FilmService с помощью Depends(get_film_service) 
@router.get('/{film_id}', response_model=Film) # Позже подключим роутер к корневому роутеру   /api/v1/film/some_id
async def film_details(film_id: str, film_service: FilmService = Depends(get_film_service)) -> Film: 
    # В сигнатуре функции указываем тип данных, получаемый из адреса запроса (film_id: str) 
    # И указываем тип возвращаемого объекта — Film
    # "get_persons_films_list-/api/v1/persons/046b28db-3db5-4ba8-8867-136b19624c7a/films-page[number]-1-page[size]-2-sort-id"
    redis_key = f"movies-get-film-/api/v1/films/{film_id}"
    print(redis_key)
    film = await film_service.get_by_id(redis_key, film_id)
    if not film:
        # Если фильм не найден, отдаём 404 статус
        print('not film', HTTPStatus.NOT_FOUND)
        print(HTTPException(status_code=HTTPStatus.NOT_FOUND, detail='film not found'))
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail='film not found')
    #return Film(id=film.id, title=film.title)
    print(type(film))
    #film.json()
    #print(film.id)
    return film #Film(id=film.id)


# http://127.0.0.1:8104/api/v1/films?filter[genre]=Comedy&page[size]=3&page[number]=6&sort=-imdb_rating&sort=created
#@router.get('/', response_model=AllFilms)
@router.get('/')
async def get_film_list(request: Request,
                        # sort: str = None,
                        filter_by: str = None,
                        pagination: PaginateModel = Depends(PaginateModel)
):

    # http://127.0.0.1:8105/api/v1/films/?filter[genre]=Comedy&page[size]=3&page[number]=6&sort=imdb_rating&sort=-created
    # output {"imdb_rating":"asc","created":"desc"}
    sorts = [v[1] for v in filter(lambda s: s[0] == 'sort', request.query_params.__dict__['_list'])]
    s_o = {}
    for s in sorts:
        if len(s) > 1:
            if s[0] == '-':
                s_o[s[1:]] = 'desc'
            else:
                s_o[s] = 'asc'
    return s_o


class SortModel:
    def __init__(self, request: Request):
        pass
# http://127.0.0.1:8104/api/v1/films/?filter=horror&page[number]=5&page[size]=21
# @router.get('/', response_model=AllFilms)
# async def get_film_list(sort: str = None,
#                         filter_by: None,
#                         pagination: PaginateModel = Depends(PaginateModel),
#                         film_service: FilmService = Depends(get_film_service)
# ):  
#     pass
    #film = await film_service.
    #film = await film_service.get_all_films()
    #print(request.url)
    #print(request.base_url.path)
    #obj = {'page_num': str(pagination.page_number), 'page_size': str(pagination.page_size), 'source': pagination.paginate_list(['1','a','b','c','c','sss', 'fff','ggg', ''])}
    # stop = pagination.page_size * pagination.page_number
    # start = stop - pagination.page_size
    # print(request.url_path_for('/'))
    # return obj.get('source')[start:stop]
    # return pagination.paginate_list(obj.get('source'))
    #return obj


# # TODO search films 2. Поиск
# @router.get('/search', response_model=AllShortOutput) # /api/v1/films/search/
# async def get_film_by_match_words(query: str,
#                                   sort: str = None,
#                                   ):
#     pass
