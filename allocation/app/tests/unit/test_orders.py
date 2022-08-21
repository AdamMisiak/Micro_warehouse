# pylint: disable=W0613
# unused-argument


def test_create_order(client):
    body = {"sku": "BIG-TABLE", "quantity": 10}
    response_body = body | {"id": 1}
    response = client.post("/api/v1/orders/", json=body)

    assert response.status_code == 200
    assert isinstance(response.json(), dict)
    assert response.json() == response_body
