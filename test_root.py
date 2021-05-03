from starlette.responses import Response
from starlette.testclient import TestClient

from api import API
from routes import ROUTE_ROOT


def test_root():
    app = API()
    client = TestClient(app)
    response: Response = client.get(ROUTE_ROOT)
    assert response.status_code == 200
