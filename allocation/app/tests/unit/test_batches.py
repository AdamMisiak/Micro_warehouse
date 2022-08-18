# pylint: disable=W0613
# unused-argument
from app.utils import settings


def test_get_batches(client):
    response = client.get("/api/v1/batches")
    print(response.json())
    assert response.status_code == 200
