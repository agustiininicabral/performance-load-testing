from fastapi.testclient import TestClient

from load_testing.app import app


client = TestClient(app)


def test_health_endpoint():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_products_endpoint_returns_requested_limit():
    response = client.get("/products", params={"limit": 5})
    assert response.status_code == 200
    payload = response.json()
    assert len(payload) == 5
    assert payload[0]["id"] == 1


def test_products_endpoint_rejects_out_of_range_limit():
    assert client.get("/products", params={"limit": 0}).status_code == 422
    assert client.get("/products", params={"limit": 101}).status_code == 422


def test_compute_endpoint_returns_deterministic_checksum():
    first = client.post("/compute", json={"iterations": 1000})
    second = client.post("/compute", json={"iterations": 1000})
    assert first.status_code == 200
    assert first.json() == second.json()
    assert first.json()["iterations"] == 1000


def test_compute_endpoint_validates_iteration_bounds():
    assert client.post("/compute", json={"iterations": 0}).status_code == 422
    assert client.post("/compute", json={"iterations": 50001}).status_code == 422
    assert client.post("/compute", json={}).status_code == 200


def test_products_endpoint_default_limit():
    response = client.get("/products")
    assert response.status_code == 200
    assert len(response.json()) == 20
