from starlette.authentication import requires
from starlette.requests import Request
from starlette.routing import Route

import config
import routes

RIDDLE_3_MSG = """

"""


@requires('authenticated')
async def info(request: Request):
    raise NotImplementedError()


@requires('authenticated')
async def solution(request: Request):
    raise NotImplementedError()


ROUTES = [
    Route(
        path=f'{routes.ROUTE3}',
        endpoint=info,
        methods=['GET'],
    ),
    Route(
        path=f'{routes.ROUTE3}',
        endpoint=solution,
        methods=['POST'],
    ),
]
