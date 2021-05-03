import base64
import binascii
import logging

from starlette.authentication import (
    AuthCredentials, AuthenticationBackend,
    AuthenticationError, SimpleUser,
)

from user import get_user_data


def _check_user_authorization(username: str, password: str) -> bool:
    log = logging.getLogger('_check_user_authorization')
    try:
        data = get_user_data(username)
        return data['password'] == password
    except Exception as ex:
        log.warning(ex)
        return False


class BasicAuthBackend(AuthenticationBackend):
    async def authenticate(self, request):
        if "Authorization" not in request.headers:
            return

        auth = request.headers["Authorization"]
        try:
            scheme, credentials = auth.split()
            if scheme.lower() != 'basic':
                return
            decoded = base64.b64decode(credentials).decode("ascii")
        except (ValueError, UnicodeDecodeError, binascii.Error) as exc:
            raise AuthenticationError('Invalid basic auth credentials')

        username, _, password = decoded.partition(":")
        if not _check_user_authorization(username, password):
            return
        else:
            return AuthCredentials(["authenticated"]), SimpleUser(username)
