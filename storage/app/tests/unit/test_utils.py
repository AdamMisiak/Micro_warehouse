import json


def test_create_user(client):
    response = client.get("/api/v1/utils/queues")
    print(response.request.url)
    print(response.request.url)
    print(response.json())
    assert response.status_code == 200

    # TODO: Add make command to run in daeom and start tests pytest -l -v -s
