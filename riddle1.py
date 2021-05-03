import codecs
import json

from starlette.authentication import requires
from starlette.requests import Request
from starlette.responses import JSONResponse
from starlette.routing import Route

import config
import routes
from config import riddle_url
from routes import ROUTE2
from response import error_response

RIDDLE_1_SECRET = 'riddle nr 1 secret for {username}'


@requires('authenticated')
async def info(request: Request):
    """
    ROT13 riddle
    :param request:
    :return:
    """

    # username = request.path_params['username']
    username = request.user.display_name
    cyphertext = codecs.encode(
        RIDDLE_1_SECRET.format(username=username),
        'rot_13'
    )
    return JSONResponse(
        dict(
            cyphertext=cyphertext
        )
    )


@requires('authenticated')
async def solution(request: Request):
    def _verify_solution(un: str, sl: str):
        encoded_data = codecs.encode(
            sl.format(un),
            'rot_13'
        )
        return str(encoded_data) == RIDDLE_1_SECRET

    username = request.path_params['username']
    try:
        body = await request.json()
        solution = body['solution']
    except json.JSONDecodeError:
        return error_response('received malformed JSON data')
    except KeyError:
        return error_response('expected JSON format:{"solution":"<solution>"}')

    if _verify_solution(username, solution):
        # TODO
        next_riddle_url = riddle_url(ROUTE2)
        response_data = dict(
            solution_correct=True,
            next_riddle=next_riddle_url,
        )
    else:
        response_data = dict(
            solution_correct=False,
            received_data=body
        )

    return JSONResponse(response_data)


ROUTES = [
    Route(
        path=f'{routes.ROUTE1}',
        endpoint=info,
        methods=['GET'],
    ),
    Route(
        path=f'{routes.ROUTE1}',
        endpoint=solution,
        methods=['POST'],
    ),
]
