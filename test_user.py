import os

from requests import Response
from starlette.testclient import TestClient

from api import API
from config import USER_DATA_PATH
from routes import ROUTE_REGISTER


def test_user_register_info_get():
    app = API()
    client = TestClient(app)
    response: Response = client.get(ROUTE_REGISTER)
    assert response.status_code == 200

def test_user_register_bogus_mail_address():
    app = API()
    client = TestClient(app)

    data = dict(
        username='bad_mail@gmail.com'
    )

    response: Response = client.post(ROUTE_REGISTER,data)
    assert response.status_code == 200

    # TODO



def test_user_register_info_post():
    import uuid
    base_path = f'/tmp/riddle-api-test-{uuid.uuid4()}'
    os.makedirs(base_path, exist_ok=True)
    app = API(base_path=base_path)
    client = TestClient(app)

    data = dict(
        username='testuser@example.com'
    )
    response: Response = client.post(ROUTE_REGISTER, data)
    assert response.status_code == 405
    assert os.path.exists(f'{USER_DATA_PATH}/testuser@example.com')
