from collections import namedtuple
from typing import Optional
from fastapi import Query


class QueryFilterModel:
    def __init__(self,
                 filter_by_genre: Optional[str] = Query(default=None, alias='filter[genre]'),
                 filter_by_director: Optional[str] = Query(default=None, alias='filter[director]')):

        self.filter_by_genre = filter_by_genre
        self.filter_by_director = filter_by_director  # TODO now innactive

    def check_if_filter(self) -> namedtuple:
        filter_selector = {'genre': self.filter_by_genre,
                           'director': self.filter_by_director}
        for name, value in filter_selector.items():
            if value is not None:
                return namedtuple('Filter', name=name, value=value)
        return None
        # return any(self.filter_by_genre, self.filter_by_director)

    def get_filter_for_elastic(self):
        filter_by = self.check_if_filter()
        if filter_by is not None:
            return {filter_by.name: filter_by.value}
        return None

    def get_filter_from_mongo_db(self):
        pass
