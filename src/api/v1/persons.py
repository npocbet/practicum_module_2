from http import HTTPStatus
from pprint import pprint

from fastapi import APIRouter, Depends, Request, HTTPException
from models.film import Person
from models.paginators import PaginateModel
from models.query_filters import QueryFilterModel

import services


router = APIRouter()
