from collections import namedtuple
from pprint import pprint
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
        print('\n\n\n\n\n')
        pprint(filter_selector)
        for name, value in filter_selector.items():
            print(name, value)
            if value is not None:
                filter = namedtuple('Filter', ['name', 'value'])
                return filter(name, value)
        return None
        # return any(self.filter_by_genre, self.filter_by_director)

    def get_filter_for_elastic(self):
        filter_by = self.check_if_filter()
        if filter_by is not None:
            return {filter_by.name: filter_by.value}
        return None

    def get_filter_from_mongo_db(self):
        pass
