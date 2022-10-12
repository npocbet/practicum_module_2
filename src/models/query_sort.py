
#from fastapi import Request


@router.get('/')
async def get_film_list(request: Request,
                        # sort: str = None,
                        filter_by: str = None,
                        pagination: PaginateModel = Depends(PaginateModel)
):

    # http://127.0.0.1:8105/api/v1/films/?filter[genre]=Comedy&page[size]=3&page[number]=6&sort=imdb_rating&sort=-created
    # output {"imdb_rating":"asc","created":"desc"}
    sorts = [v[1] for v in filter(lambda s: s[0] == 'sort', request.query_params.__dict__['_list'])]
    s_o = {}
    for s in sorts:
        if len(s) > 1:
            if s[0] == '-':
                s_o[s[1:]] = 'desc'
            else:
                s_o[s] = 'asc'
    return s_o
