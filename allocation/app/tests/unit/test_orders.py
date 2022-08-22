# pylint: disable=W0613
# unused-argument
import pytest
from app.utils import exceptions


def test_create_order(client):
    body = {"sku": "BIG-TABLE", "quantity": 10}
    response_body = body | {"id": 1}
    response = client.post("/api/v1/orders/", json=body)

    assert response.status_code == 200
    assert isinstance(response.json(), dict)
    assert response.json() == response_body


def test_get_orders(client, order):
    response = client.get("/api/v1/orders")

    assert response.status_code == 200
    assert isinstance(response.json(), list)
    assert len(response.json()) == 1
    assert response.json()[0].get("id") == 1
    assert response.json()[0].get("sku") == "BIG-TABLE"
    assert response.json()[0].get("quantity") == 10


def test_get_order(client, order):
    response = client.get("/api/v1/orders/1")

    assert response.status_code == 200
    assert isinstance(response.json(), dict)
    assert response.json().get("id") == 1
    assert response.json().get("sku") == "BIG-TABLE"
    assert response.json().get("quantity") == 10


def test_allocate_order(client, order, batch):
    response = client.get("/api/v1/orders/1/allocate")

    assert response.status_code == 200
    assert isinstance(response.json(), dict)
    assert response.json().get("id") == 1
    assert response.json().get("sku") == "BIG-TABLE"
    assert response.json().get("quantity") == 0


def test_allocate_order_with_missing_order(client, batch):
    with pytest.raises(exceptions.OrderNotFound) as excinfo:
        client.get("/api/v1/orders/1/allocate")
    assert "Order not found" in str(excinfo.value)


def test_allocate_order_already_allocated(client, order, batch):
    response = client.get("/api/v1/orders/1/allocate")
    assert response.status_code == 200

    with pytest.raises(exceptions.OrderAlreadyAllocated) as excinfo:
        client.get("/api/v1/orders/1/allocate")
    assert "Order is already allocated" in str(excinfo.value)


def test_allocate_order_with_missing_batch(client, order):
    with pytest.raises(exceptions.InvalidSku) as excinfo:
        client.get("/api/v1/orders/1/allocate")
    assert "Invalid sku BIG-TABLE" in str(excinfo.value)


def test_allocate_order_with_wrong_quantity(client, order_wrong_quantity, batch):
    response = client.get("/api/v1/orders/1/allocate")

    assert response.status_code == 200
    assert isinstance(response.json(), dict)
    assert response.json().get("event_type") == "OutOfStock"
    assert response.json().get("sku") == "BIG-TABLE"
