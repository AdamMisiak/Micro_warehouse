# pylint: disable=W0613
# unused-argument
from app.utils import settings


def test_read_queues(client, queue):
    response = client.get("/api/v1/utils/queues")

    assert response.status_code == 200
    assert isinstance(response.json(), list)
    assert {"url": "http://localhost:4566/000000000000/micro-warehouse-external-queue"} in response.json()


def test_read_queue(client, queue):
    response = client.get(f"/api/v1/utils/queue/{settings.QUEUE_NAME}")

    assert response.status_code == 200
    assert isinstance(response.json(), dict)
    assert "attributes" in response.json().keys()
    assert "http://localhost:4566/000000000000/micro-warehouse-external-queue" in response.json().values()


def test_read_messages(client, queue):
    response = client.get("/api/v1/utils/messages", params={"queue_name": settings.QUEUE_NAME})

    assert response.status_code == 200
    assert isinstance(response.json(), list)


def test_create_queue(client):
    response = client.get("/api/v1/utils/queues", params={"name": settings.QUEUE_NAME, "delay": 0, "visibility": 60})

    assert response.status_code == 200
    assert isinstance(response.json(), list)
    assert {"url": "http://localhost:4566/000000000000/micro-warehouse-external-queue"} in response.json()
