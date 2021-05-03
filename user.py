import codecs
import json
import os
import re

from starlette.authentication import requires
from starlette.requests import Request
from starlette.responses import JSONResponse, PlainTextResponse
from starlette.routing import Route

import config
import routes
from response import error_response

MAIL_RGX = re.compile(r'^[a-z]+\.[a-z]+@example\.com$')
REGISTER_INFO_MSG = """    On this endpoint you can register your user. 
    You are required to do this in order to participate in the game. 
    The only usernames accepted are *@example.com mail addresses. 
    Send a PUT request to this endpoint with the following JSON payload' 
    and substitute your email address: 
    {"username":"<your email address>"} 
    After registration, your login data will be sent via eMail. 

    From this point on, you can query your user data 
    at the /user/your_username endpoint.
    You will need to provide HTTP BASIC login credentials for this,
    that means you need to send an "Authorization" header
    along with the request, that contains your base64 encoded 
    "username:password" token. For example curl, wget and
    python requests all can handle this for you.\n"""


class UserNotFoundException(Exception):
    pass


def info(request: Request):
    return PlainTextResponse(REGISTER_INFO_MSG)


def _sanitize_mail_addr(mail_addr: str):
    if not MAIL_RGX.match(mail_addr):
        raise ValueError(
            'Mail address must be an foo.bar@example.com address'
        )

    if os.path.exists(os.path.join(config.USER_DATA_PATH, mail_addr)):
        raise ValueError(f'user {mail_addr} exists')


async def register(request: Request):
    # returns:
    #   * pgp encrypted cyphertext for 'grand solution'
    #   * cyphertext encrypting URL for riddle 1
    try:
        payload = json.loads(await request.body())
        username: str = payload['username']
    except json.JSONDecodeError as err:
        return error_response(str(err))
    except KeyError:
        return error_response(
            'expected JSON formatted data in the form '
            '{"username":"<your_mail_address>"}'
        )
    else:
        username = username.lower()
        try:
            _sanitize_mail_addr(username)
        except ValueError as ex:
            return error_response(str(ex))
        else:
            user_data = register_user(username)

            return JSONResponse(
                dict(
                    status='success',
                    user_data=user_data,
                    next_riddle=config.riddle_url(routes.ROUTE1)
                )
            )


@requires('authenticated')
async def query(request: Request):
    try:
        username = request.path_params['username']
        user_data = get_user_data(username)
    except KeyError:
        return error_response(f'username could not be found')
    except Exception as ex:
        return error_response(str(ex))

    return JSONResponse(user_data)


def unlock_level(username: str, level_id: str):
    data = get_user_data(username)
    data['unlocked_levels'] = {
        *data['unlocked_levels'],
        level_id
    }
    save_user_data(username, data)


def save_user_data(username: str, data: dict):
    file_path = os.path.join(config.USER_DATA_PATH, username)
    with open(file_path, 'w+') as fh:
        json.dump(data, fh)


def treasure_for_user(username: str) -> str:
    with open(config.TREASURE_PATH, 'r') as fh:
        treasure_text = fh.readline()
        # TODO encrypt for user?

    return treasure_text


def register_user(username: str):
    data = dict(
        username=username,
        password=codecs.encode(username, 'rot_13'),
        treasure=treasure_for_user(username),
        unlocked_levels={},
    )
    save_user_data(username, data)
    return data


def get_user_data(username: str) -> dict:
    file_path = os.path.join(config.USER_DATA_PATH, username)
    try:
        with open(file_path, 'r') as fb:
            return json.load(fb)
    except FileNotFoundError:
        raise UserNotFoundException()


ROUTES = [
    Route(
        path=f'{routes.ROUTE_REGISTER}',
        endpoint=info,
        methods=['GET'],
    ),
    Route(
        path=f'{routes.ROUTE_REGISTER}',
        endpoint=register,
        methods=['POST'],
    ),
]
