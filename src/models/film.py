import logging
from pprint import pprint
from typing import Dict, List, Optional
import orjson
#from uuid import uuid4
import uuid
# Используем pydantic для упрощения работы при перегонке данных из json в объекты
from pydantic import BaseModel, Field, ValidationError


def orjson_dumps(v, *, default):
    # orjson.dumps возвращает bytes, а pydantic требует unicode, поэтому декодируем
    return orjson.dumps(v, default=default).decode()


class UUIDMixin(BaseModel):
    id: uuid.UUID
    class Config:
        # Заменяем стандартную работу с json на более быструю
        # json_encoders = {id: uuid4}
        json_loads = orjson.loads
        json_dumps = orjson_dumps


class UUIDNameMixin(UUIDMixin):
    name: str


class Film(UUIDMixin):
    """подробная информация о фильме
       /api/v1/films/<uuid:UUID>/
    """
    title: str
    description: Optional[str] = ''
    imdb_rating: Optional[float] = Field(default=0.0, example=88.41)
    genre: Optional[List[str]] = Field(example=['Comedy', 'Fantasy'])
    director: List[str]
    actors_names: Optional[List[str]] = []
    writers_names: Optional[List[str]] = []
    actors: Optional[List[UUIDNameMixin]] = []
    writers: Optional[List[UUIDNameMixin]] = []


class FilmShort(UUIDMixin):
    """
       Поиск, фильтр и отображение фильмов на главной странице.
       GET /api/v1/films?sort=-imdb_rating&page[size]=50&page[number]=1
       GET /api/v1/films/search/
       GET /api/v1/persons/<uuid:UUID>/film/ фильмы в которых учавствовал person.
       Жанр и популярные фильмы в нём. Это просто фильтрация.
       /api/v1/films?sort=-imdb_rating&filter[genre]=<comedy-uuid>
    """
    title: str
    imdb_rating: Optional[float] = Field(default=0.0, example=88.41)


class AllFilms(BaseModel):
    results: List[FilmShort]


class AllShortFilms(BaseModel):
    page_size: int
    page_number: int
    filter: Optional[dict] = {}
    sort: Optional[dict] = {}
    results: List[FilmShort]
    amount_results: Optional[int] = 0


class Person(UUIDMixin):
    """/api/v1/persons/search/
       Данные по персоне."""
    role: str
    full_name: str
    film_ids: Optional[List[UUIDMixin]] = []


class Genre(UUIDNameMixin):
    """Данные по конкретному жанру.
       /api/v1/genres/<uuid:UUID>/ 
    """
    # name = str

class AllGenres(BaseModel):
    results: List[Genre] = []

    class Config:
        json_loads = orjson.loads
        json_dumps = orjson_dumps


class GenrePopularFilms(Genre):
    # TODO выбрать правильный URL
    """
        Популярные фильмы в жанре.
        /api/v1/films...
    """
    top_films: List[FilmShort]

    class Config:
        json_loads = orjson.loads
        json_dumps = orjson_dumps


genres = {'id': 'bccbbbb6-be40-44f5-a025-204bcfcf2667',
                          'name': 'Raphael Sbarge'}

# try:
#     g = Genre.parse_obj(genres)
#     print('\ngenres',g)
# except ValidationError as e:
#     print('genre', e.json())


pers = {
  "id": "58060969-dce4-4a19-a94f-381d263e554c",
  "name": "str",
      "role": "str",
      "film_ids": [{"id":"58060969-dce4-4a19-a94f-381d263e554c"}]
      }

# try:
#   person = Person.parse_obj(pers)
#   print('\npers', person)
#   print('\n')
# except ValidationError as ee:
#   print('pers', ee.json())


# try:
#     biggest = Film.parse_obj(big.get('_source'))
#     pprint(biggest)
# except ValidationError as v:
#     print('big', v.json())
