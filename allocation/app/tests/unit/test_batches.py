# pylint: disable=W0613
# unused-argument


def test_create_batch(client):
    body = {"sku": "BIG-TABLE", "reference": "batch1", "quantity": 10}
    response_body = body | {"eta": None, "id": 1}
    response = client.post("/api/v1/batches/", json=body)

    assert response.status_code == 200
    assert isinstance(response.json(), dict)
    assert response.json() == response_body


def test_update_batch(client, batch):
    response_batch_info = client.get("/api/v1/batches/1")
    assert response_batch_info.json()["sku"] == "BIG-TABLE"
    assert response_batch_info.json()["reference"] == "batch1"

    body = {"sku": "SMALL-TABLE", "reference": "batch2", "quantity": 10}
    response = client.put("/api/v1/batches/1", json=body)

    assert response.status_code == 200
    assert isinstance(response.json(), dict)
    assert response.json()["status_code"] == 200
    assert response.json()["message"] == "Batch id: 1 has been updated"

    response_batch_info = client.get("/api/v1/batches/1")
    assert response_batch_info.json()["sku"] == body["sku"]
    assert response_batch_info.json()["reference"] == body["reference"]


def test_get_batch(client, batch):
    response = client.get("/api/v1/batches/1")

    assert response.status_code == 200
    assert isinstance(response.json(), dict)
    assert response.json().get("id") == 1
    assert response.json().get("sku") == "BIG-TABLE"
    assert response.json().get("reference") == "batch1"
    assert response.json().get("quantity") == 10


def test_get_batches(client, batch):
    response = client.get("/api/v1/batches")

    assert response.status_code == 200
    assert isinstance(response.json(), list)
    assert response.json()[0].get("id") == 1
    assert response.json()[0].get("sku") == "BIG-TABLE"
