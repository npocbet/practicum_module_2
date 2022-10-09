from http import HTTPStatus
from pprint import pprint

from fastapi import APIRouter, Depends, Request, HTTPException
from models.film import AllGenres, Genre, GenrePopularFilms
from models.paginators import PaginateModel
from models.query_filters import QueryFilterModel

from services.genres import GenreService, get_genre_service


router = APIRouter()


@router.get('', response_model=AllGenres)  #/api/openapi
async def get_genres(sort: str = None,
                     filter_by: QueryFilterModel = Depends(QueryFilterModel),
                     pagination: PaginateModel = Depends(PaginateModel),
                     genre_service: GenreService = Depends(get_genre_service)):

    redis_key = "api/v1/genres"
    genres = await genre_service.get_genres(redis_key)
    if not genres:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail='film not found')
    
    genre_name_id = [{"id":genre.get('_id'), "name": genre.get('_source').get("name")} for genre in genres['hits']['hits']]
    output = AllGenres(results=genre_name_id)
    #return {"results": []} # output
    output.json()
    return output
