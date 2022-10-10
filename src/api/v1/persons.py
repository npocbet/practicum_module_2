from http import HTTPStatus
from fastapi import APIRouter, Depends, HTTPException
from models.film import Person
from services.persons import PersonService, get_persons_service

router = APIRouter()


@router.get('/{person_id}', response_model=Person)
async def person_details(person_id: str, person_service: PersonService = Depends(get_persons_service)) -> Person:
    # TODO: ХЗ как тут
    redis_key = f"movies-get-film-/api/v1/films/{person_id}"
    person = await person_service._get_person_by_id(person_id)
    if not person:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail='person not found')
    return person
