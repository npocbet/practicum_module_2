#from typing import uuid
import logging
from pprint import pprint
from typing import List, Optional
import orjson
#from uuid import uuid4
import uuid
# Используем pydantic для упрощения работы при перегонке данных из json в объекты
from pydantic import BaseModel, ValidationError


def orjson_dumps(v, *, default):
    # orjson.dumps возвращает bytes, а pydantic требует unicode, поэтому декодируем
    return orjson.dumps(v, default=default).decode()


class UUIDMixin(BaseModel):
    id: uuid.UUID


class UUIDNameMixin(UUIDMixin):
    name: str


class Film(UUIDMixin):
    """подробная информация о фильме
       /api/v1/films/<uuid:UUID>/
    """
    title: str
    description: Optional[str] = ''
    imdb_rating: Optional[float] = 0.0
    genre: Optional[List] = []
    director: List[str]
    actors_names: Optional[List[str]] = []
    writers_names: Optional[List[str]] = []
    actors: List[UUIDNameMixin] = []
    writers: List[UUIDNameMixin] = []

    class Config:
        # Заменяем стандартную работу с json на более быструю
        # json_encoders = {id: uuid4}
        json_loads = orjson.loads
        json_dumps = orjson_dumps


class AllFilms(BaseModel):
    all_films: List[Film]


class FilmShort(UUIDMixin):
    """
       Поиск, фильтр и отображение фильмов на главной странице.
       GET /api/v1/films?sort=-imdb_rating&page[size]=50&page[number]=1
       GET /api/v1/films/search/
       GET /api/v1/persons/<uuid:UUID>/film/ фильмы в которых учавствовал person.
    """
    title: str
    imdb_rating: Optional[float] = 0.0
    class Config:
        json_loads = orjson.loads
        json_dumps = orjson_dumps


class Person(UUIDNameMixin):
    """/api/v1/persons/search/
       Данные по персоне."""
    role: str
    film_ids: Optional[List[UUIDMixin]] = []

    class Config:
        json_loads = orjson.loads
        json_dumps = orjson_dumps


class Genre(UUIDNameMixin):
    """Данные по конкретному жанру.
       /api/v1/genres/<uuid:UUID>/ 
    """
    pass
    # name = str

    # class Config:
    #     json_loads = orjson.loads
    #     json_dumps = orjson_dumps

class GenrePopularFilm(Genre):
    # TODO выбрать правильный URL
    """
        Популярные фильмы в жанре.
        /api/v1/films...
    """
    top_films: List[FilmShort]

    class Config:
        json_loads = orjson.loads
        json_dumps = orjson_dumps


# mj = """{
#   "id": "7b0bb047-c8a5-4a04-b9b1-ee4bfc07c05b",
#   "imdb_rating": 4.42,
#   "genre": [{
#     "id": "6aefeaba-e617-4e81-a152-118cf6a88c40",
#     "name": "nest a 1"
#             },{
#       "id": "362cac08-ee39-4305-be17-b9fa563eb336",
#       "name": "nest a 2"
#     }],
#   "title": "my title",
#   "description": "desc text",
#   "director": "dir dir ",
#   "actors_names": "actor1actor2",
#   "writers_names": "w1w2",
#   "actors": [{
#     "id": "6aefeaba-e617-4e81-a152-118cf6a88c40",
#     "name": "nest a 1"
#             },{
#       "id": "362cac08-ee39-4305-be17-b9fa563eb336",
#       "name": "nest a 2"
#     }],
#   "writers": [{
#     "id": "7b0ba047-c8a5-4a04-b9b1-ee4bfc07c05b",
#     "name": "nest wr 1"
#   },{
#       "id": "58060969-dce4-4a19-a94f-381d263e554c",
#       "name": "nest wr2"
#     }]
# }"""

# try:
#     film = Film.parse_raw(mj)
#     print(film)
#     print('11111111111\n')
# except ValidationError as e:
#     print(e.json())

#pprint(film.actors[1])

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





big = {'_id': '2a090dde-f688-46fe-a9f4-b781a985275e',
  '_index': 'movies',
  '_score': None,
  '_source': {'actors': [{'id': '00395304-dd52-4c7b-be0d-c2cd7a495684',
                          'name': 'Jennifer Hale'},
                         {'id': '2802ff93-f147-49cc-a38b-2f787bd2b875',
                          'name': 'John Cygan'},
                         {'id': '578593ee-3268-4cd4-b910-8a44cfd05b73',
                          'name': 'Rafael Ferrer'},
                         {'id': 'bccbbbb6-be40-44f5-a025-204bcfcf2667',
                          'name': 'Raphael Sbarge'}],
              'actors_names': ['Jennifer Hale',
                               'John Cygan',
                               'Rafael Ferrer',
                               'Raphael Sbarge'],
              'description': 'Four thousand years before the fall of the '
                             'Republic, before the fall of the Jedi, a great '
                             'war was fought, between the armies of the Sith '
                             'and the forces of the Republic. A warrior is '
                             'chosen to rescue a Jedi with a power important '
                             'to the cause of the Republic, but in the end, '
                             'will the warrior fight for the Light Side of the '
                             'Force, or succumb to the Darkness?',
              'director': ['Casey Hudson'],
              'genre': ['Action', 'Adventure', 'Fantasy'],
              'id': '2a090dde-f688-46fe-a9f4-b781a985275e',
              'imdb_rating': 9.6,
              'title': 'Star Wars: Knights of the Old Republic',
              'writers': [{'id': '1bc82e3e-d9ea-4da0-a5ea-69ba20b94373',
                           'name': 'Lukas Kristjanson'},
                          {'id': '1e8d746d-72d2-4da2-ad20-651154cfb158',
                           'name': 'Michael Gallo'},
                          {'id': '61bffbdc-910e-47b9-8b04-43b5f27807b4',
                           'name': 'James Ohlen'},
                          {'id': '63a787ba-dd3f-4176-a894-9970b5c43a12',
                           'name': 'Drew Karpyshyn'},
                          {'id': '8778550c-90c6-4180-a6ac-eba956f0ce59',
                           'name': 'David Gaider'},
                          {'id': '91c4ca66-e3e1-4932-8447-aadd67fd67b1',
                           'name': 'Peter Thomas'},
                          {'id': 'b29e255d-644d-4e16-9018-c1bcb49934e5',
                           'name': 'Lynn Taylor'},
                          {'id': 'f7337af0-21aa-445f-aecf-4794c0faa811',
                           'name': 'Brett Rector'}],
              'writers_names': ['Lukas Kristjanson',
                                'Michael Gallo',
                                'James Ohlen',
                                'Drew Karpyshyn',
                                'David Gaider',
                                'Peter Thomas',
                                'Lynn Taylor',
                                'Brett Rector']},
  '_type': '_doc',
  'sort': [9.6]}


# try:
#     biggest = Film.parse_obj(big.get('_source'))
#     pprint(biggest)
# except ValidationError as v:
#     print('big', v.json())



# class LALALAND(UUIDNameMixin):
#     pass

# ooo = {'id': '1e8d746d-72d2-4da2-ad20-651154cfb158',
#        'name': 'Michael Gallo'}
# try:
#     lala = LALALAND.parse_obj(ooo)
#     print('\nlalal', lala)
# except ValidationError as vvv:
#     print(vvv.json())
