# pylint: disable=W0613
# unused-argument


def test_get_batches(client, batch):
    response = client.get("/api/v1/batches")

    assert response.status_code == 200
    assert isinstance(response.json(), list)
    assert response.json()[0].get("id") == 1
    assert response.json()[0].get("sku") == "BIG-TABLE"


def test_create_batch(client):
    body = {"sku": "BIG-TABLE", "reference": "batch1", "quantity": 10}
    response_body = body | {"eta": None, "id": 1}
    response = client.post("/api/v1/batches/", json=body)

    assert response.status_code == 200
    assert isinstance(response.json(), dict)
    assert response.json() == response_body
