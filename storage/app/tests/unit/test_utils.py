import localstack_client.session as boto3
from app.utils import settings


def test_read_queues(client, queue):
    response = client.get("/api/v1/utils/queues")
    print(response.json())

    assert response.status_code == 200
    assert type(response.json()) == list
    assert {"url": "http://localhost:4566/000000000000/micro-warehouse-external-queue"} in response.json()
