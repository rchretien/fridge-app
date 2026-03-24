"""API tests for utility endpoints."""

import httpx
from fastapi.testclient import TestClient


def test_get_product_type_list(client: TestClient) -> None:
    """Ensure the product type list endpoint returns seeded values."""
    response = client.get("/utils/product_type_list")
    assert response.status_code == httpx.codes.OK

    body = response.json()
    assert len(body["product_type_list"]) >= 1
    assert any("poultry" in item["name"].lower() for item in body["product_type_list"])


def test_get_product_location_list(client: TestClient) -> None:
    """Ensure the product location endpoint returns the expected locations."""
    response = client.get("/utils/product_location_list")
    assert response.status_code == httpx.codes.OK

    body = response.json()
    assert len(body["product_location_list"]) == 3
    assert {item["name"] for item in body["product_location_list"]} == {
        "refrigerator",
        "big freezer",
        "small freezer",
    }
