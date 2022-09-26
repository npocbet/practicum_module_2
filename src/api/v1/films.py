from http import HTTPStatus

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel

from services.film import FilmService, get_film_service


router = APIRouter() # Объект router, в котором регистрируем обработчики

# Модель ответа API
# https://pydantic-docs.helpmanual.io
# У неё есть встроенные механизмы валидации, сериализации и десериализации
class Film(BaseModel):
    id: str
    title: str


# Внедряем FilmService с помощью Depends(get_film_service) 
@router.get('/{film_id}', response_model=Film) # Позже подключим роутер к корневому роутеру   /api/v1/film/some_id
async def film_details(film_id: str, film_service: FilmService = Depends(get_film_service)) -> Film: 
    # В сигнатуре функции указываем тип данных, получаемый из адреса запроса (film_id: str) 
    # И указываем тип возвращаемого объекта — Film
    film = await film_service.get_by_id(film_id)
    if not film:
        # Если фильм не найден, отдаём 404 статус
        # Желательно пользоваться уже определёнными HTTP-статусами, которые содержат enum  
                # Такой код будет более поддерживаемым
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail='film not found')

    # Перекладываем данные из models.Film в Film
    # Обратите внимание, что у модели бизнес-логики есть поле description 
        # Которое отсутствует в модели ответа API. 
        # Если бы использовалась общая модель для бизнес-логики и формирования ответов API
        # вы бы предоставляли клиентам данные, которые им не нужны 
        # и, возможно, данные, которые опасно возвращать
    return Film(id=film.id, title=film.title)
