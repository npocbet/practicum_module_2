#from typing import uuid
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


class NestedPeople(BaseModel):
    id: str
    name: str


class Film(BaseModel):
    id: str
    title: str
    description: str
    imdb_rating: Optional[float] = 0
    genre: Optional[List] = []
    director: str
    actors_names: str
    writers_names: str
    #sactors: List[NestedPeople]
    writers: List[NestedPeople]

    class Config:
        # Заменяем стандартную работу с json на более быструю
        # json_encoders = {id: uuid4}
        json_loads = orjson.loads
        json_dumps = orjson_dumps


mj = """{
  "id": "7b0bb047-c8a5-4a04-b9b1-ee4bfc07c05b",
  "imdb_rating": 4.42,
  "genre": ["lala"],
  "title": "my title",
  "description": "desc text",
  "director": "dir dir ",
  "actors_names": "actor1actor2",
  "writers_names": "w1w2",
  "actors": [{
    "id": "6aefeaba-e617-4e81-a152-118cf6a88c40",
    "name": "nest a 1"
            },{
      "id": "362cac08-ee39-4305-be17-b9fa563eb336",
      "name": "nest a 2"
    }],
  "writers": [{
    "id": "7b0ba047-c8a5-4a04-b9b1-ee4bfc07c05b",
    "name": "nest wr 1"
  },{
      "id": "58060969-dce4-4a19-a94f-381d263e554c",
      "name": "nest wr2"
    }]
}"""

try:
  film = Film.parse_raw(mj)
except ValidationError as e:
  print(e.json())

pprint(film.actors[0].id)
