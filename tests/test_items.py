def test_root(client):
    response = client.get("/")
    assert response.status_code == 200


def test_list_items_empty(client):
    response = client.get("/items")
    assert response.status_code == 200
    assert response.json() == []


def test_create_item(client):
    payload = {"name": "Widget", "description": "A useful widget", "price": 9.99, "quantity": 5}
    response = client.post("/items", json=payload)
    assert response.status_code == 201
    body = response.json()
    assert body["id"] == 1
    assert body["name"] == "Widget"
    assert body["price"] == 9.99
    assert body["quantity"] == 5


def test_create_item_invalid_price(client):
    payload = {"name": "Widget", "price": -1, "quantity": 5}
    response = client.post("/items", json=payload)
    assert response.status_code == 422


def test_list_items_after_create(client):
    client.post("/items", json={"name": "A", "price": 1.0, "quantity": 1})
    client.post("/items", json={"name": "B", "price": 2.0, "quantity": 2})
    response = client.get("/items")
    assert response.status_code == 200
    assert len(response.json()) == 2


def test_get_item(client):
    created = client.post("/items", json={"name": "Widget", "price": 9.99, "quantity": 5}).json()
    response = client.get(f"/items/{created['id']}")
    assert response.status_code == 200
    assert response.json() == created


def test_get_item_not_found(client):
    response = client.get("/items/999")
    assert response.status_code == 404


def test_update_item(client):
    created = client.post("/items", json={"name": "Widget", "price": 9.99, "quantity": 5}).json()
    response = client.put(f"/items/{created['id']}", json={"price": 12.5})
    assert response.status_code == 200
    body = response.json()
    assert body["price"] == 12.5
    assert body["name"] == "Widget"


def test_update_item_not_found(client):
    response = client.put("/items/999", json={"price": 12.5})
    assert response.status_code == 404


def test_delete_item(client):
    created = client.post("/items", json={"name": "Widget", "price": 9.99, "quantity": 5}).json()
    response = client.delete(f"/items/{created['id']}")
    assert response.status_code == 204

    response = client.get(f"/items/{created['id']}")
    assert response.status_code == 404


def test_delete_item_not_found(client):
    response = client.delete("/items/999")
    assert response.status_code == 404
