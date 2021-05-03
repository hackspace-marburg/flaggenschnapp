import logging
import os

from starlette.applications import Starlette
from starlette.middleware.authentication import AuthenticationMiddleware
from starlette.requests import Request
from starlette.responses import PlainTextResponse, Response
from starlette.routing import Route
from starlette.testclient import TestClient

import authentication
import config
import riddle1
import riddle2
import riddle3
import riddle4
import routes
import user
from routes import ROUTE_ROOT


class API(Starlette):
    def __init__(self,
                 host=None,
                 port=None,
                 api_proto=None,
                 log_level=None,
                 base_path=None,
                 treasure_path=None,
                 user_data_path=None,
                 winner_mail_address=None,
                 ):

        api_routes = (
            Route(routes.ROUTE_ROOT, root),
            Route(
                path=f'{routes.ROUTE_USER}/{{username}}',
                endpoint=user.query,
                methods=['GET'],
            ),
            *user.ROUTES,
            *riddle1.ROUTES,
            *riddle2.ROUTES,
            *riddle3.ROUTES,
            *riddle4.ROUTES,
        )

        super(API, self).__init__(routes=api_routes)
        log = logging.getLogger('init')

        self.add_middleware(
            AuthenticationMiddleware,
            backend=authentication.BasicAuthBackend()
        )

        if host is None:
            config.HOST = os.environ.get('HOST', '0.0.0.0')
        if port is None:
            config.PORT = int(os.environ.get('PORT', 5000))
        if api_proto is None:
            config.API_PROTO = os.environ.get('API_PROTO', 'http')
        if log_level is None:
            config.LOG_LEVEL = logging.getLevelName(
                os.environ.get('LOG_LEVEL', 'DEBUG')
            )
        if base_path is None:
            config.BASE_PATH = os.environ.get('BASE_PATH', '/tmp')

        os.makedirs(config.BASE_PATH, exist_ok=True)

        if treasure_path is None:
            config.TREASURE_PATH = os.environ.get(
                'TREASURE_PATH', f'{config.BASE_PATH}/treasure'
            )
        if user_data_path is None:
            config.USER_DATA_PATH = os.environ.get(
                'USER_DATA_PATH', f'{config.BASE_PATH}/users/'
            )
        if winner_mail_address is None:
            config.WINNER_MAIL_ADDRESS = os.environ.get(
                'WINNER_MAIL_ADDRESS', 'gewinnspiel@example.com' # TODO
            )

        if not os.path.exists(config.TREASURE_PATH):
            # TODO
            treasure_text = 'Dies ist der treasure text!'
            log.info(f'creating treasure file: {config.TREASURE_PATH}')
            with open(config.TREASURE_PATH, 'w+') as fh:
                fh.write(treasure_text)

        os.makedirs(config.USER_DATA_PATH, exist_ok=True)


async def root(request: Request):
    msg = "Hi, this is the flaggenschnapp riddle API.\n" \
          f'If you want to register, go to {routes.ROUTE_REGISTER}\n'
    return PlainTextResponse(msg)
