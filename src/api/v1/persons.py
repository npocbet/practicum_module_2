import json
from http import HTTPStatus
from fastapi import APIRouter, Depends, HTTPException
from models.film import Person, AllShortFilms, FilmShort, Persons
from models.paginators import PaginateModel
from services.persons import PersonService, get_persons_service

router = APIRouter()


@router.get('/{person_id}', response_model=Person)
async def person_details(person_id: str, person_service: PersonService = Depends(get_persons_service)) -> Person:
    # TODO: ХЗ как тут
    redis_key = f"movies-get-film-/api/v1/persons/{person_id}"
    person = await person_service.get_person_by_id(person_id)
    if not person:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail='person not found')
    return person


@router.get('/{person_id}/film/', response_model=AllShortFilms)
async def get_person_film_list(person_id: str,
                               # sort: str = None,
                               pagination: PaginateModel = Depends(PaginateModel),
                               person_service: PersonService = Depends(get_persons_service)
                               ) -> AllShortFilms:
    # TODO: актуализировать
    redis_key = f"movies-get-film-/api/v1/films/pnum:{pagination.page_number}-psize:{pagination.page_size}"
    film = await person_service.get_films_by_person_id(redis_key,
                                                       offset=pagination.offset,
                                                       limit=pagination.page_size,
                                                       person_id=person_id)

    to_res = [FilmShort(**source['_source']) for source in film]
    # with open(file='log.json', mode='w') as f:
    #     f.write(json.dumps(to_res))
    amount = len(to_res)
    responce = AllShortFilms(page_size=pagination.page_size, page_number=pagination.page_number, results=to_res,
                             amount_results=amount)
    responce.json()
    return responce


@router.get('/search/', response_model=Persons)
async def search_persons_by_query(query: str,
                                  pagination: PaginateModel = Depends(PaginateModel),
                                  person_service: PersonService = Depends(get_persons_service),
                                  ) -> Persons:
    # TODO: дописать redis
    redis_key = f"api/v1/films/search:query={query}:pnum={pagination.page_number}:psize={pagination.page_size}"
    person = await person_service.search_person_by_query(redis_key=redis_key, query=query, pagination=pagination)
    if not person:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail='persons by query not found')
#    search_res = [FilmShort(**source['_source']) for source in person['hits']['hits']]
    search_res = person
 #   amount = person['hits']['total']['value']
    amount = len(person)
    responce = Persons(results=search_res, amount_results=amount, page_size=pagination.page_size,
                       page_number=pagination.page_number)
    responce.json()
    return responce
