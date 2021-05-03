from starlette.authentication import requires
from starlette.requests import Request
from starlette.routing import Route

import config
import routes

RIDDLE_2_MSG = """

"""


@requires('authenticated')
async def info(request: Request):
    pass


@requires('authenticated')
async def solution(request: Request):
    """
    polynomial Aufgabe

    x = 62
    x^3 = 238328
    x^3 = (a*10^5 + b*10^4 + c*10^3 + b*10^2 + a*10^1 + c*10^0)
    x = (a*10^5 + b*10^4 + c*10^3 + b*10^2 + a*10^1 + c*10^0)^(1/3)


    """

    raise NotImplementedError()


ROUTES = [
    Route(
        path=f'{routes.ROUTE2}',
        endpoint=info,
        methods=['GET'],
    ),
    Route(
        path=f'{routes.ROUTE2}',
        endpoint=solution,
        methods=['POST'],
    ),
]
