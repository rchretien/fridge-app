"""Tests for the server-rendered inventory UI."""

from datetime import datetime, timedelta
from typing import Any

import httpx
from fastapi.testclient import TestClient

from fridge_app_backend.config import config
from fridge_app_backend.orm.enums.base_enums import (
    ProductLocationEnum,
    ProductTypeEnum,
    ProductUnitEnum,
)


def _html_form_payload(**overrides: Any) -> dict[str, str]:
    """Build form-urlencoded data for the mobile HTML forms."""
    payload = {
        "product_name": "Greek Yogurt",
        "description": "Protein-rich yogurt",
        "quantity": "2",
        "unit": ProductUnitEnum.BOXES.value,
        "expiry_date_date": (datetime.now(tz=config.brussels_tz) + timedelta(days=5)).strftime(
            "%Y-%m-%d"
        ),
        "product_location": ProductLocationEnum.REFRIGERATOR.value,
        "product_type": ProductTypeEnum.DAIRY.value,
    }
    payload.update(overrides)
    return payload


def _create_product_through_api(client: TestClient, product_name: str) -> int:
    """Create a product through the JSON API and return its identifier."""
    payload = {
        "product_name": product_name,
        "description": f"{product_name} description",
        "quantity": 1,
        "unit": ProductUnitEnum.BOXES.value,
        "expiry_date": (datetime.now(tz=config.brussels_tz) + timedelta(days=4)).isoformat(),
        "product_location": ProductLocationEnum.REFRIGERATOR.value,
        "product_type": ProductTypeEnum.FRUIT.value,
    }
    response = client.post("/inventory/create", json=payload)
    assert response.status_code == httpx.codes.CREATED
    return response.json()["product_id"]


def test_home_page_renders_welcome_dashboard(client: TestClient) -> None:
    """The root page should render the welcome dashboard instead of the full inventory grid."""
    response = client.get("/")

    assert response.status_code == httpx.codes.OK
    assert "Welcome back" in response.text
    assert "Open inventory" in response.text
    assert 'id="inventory-controls"' not in response.text
    assert "Home" in response.text


def test_inventory_page_renders_mobile_controls(client: TestClient) -> None:
    """The dedicated inventory page should expose the table controls and add action."""
    response = client.get("/web/inventory")

    assert response.status_code == httpx.codes.OK
    assert 'id="inventory-controls"' in response.text
    assert "Add product" in response.text
    assert "Inventory" in response.text
    assert "More" in response.text


def test_inventory_list_fragment_filters_by_name_prefix(client: TestClient) -> None:
    """The HTMX list fragment should respect the name prefix filter."""
    _create_product_through_api(client, "Apple Juice")
    _create_product_through_api(client, "Bananas")

    response = client.get("/web/inventory/list", params={"q": "App"})

    assert response.status_code == httpx.codes.OK
    assert "Apple Juice" in response.text
    assert "Bananas" not in response.text


def test_inventory_list_fragment_renders_load_more_when_needed(client: TestClient) -> None:
    """The list fragment should render a load-more button when not all rows are shown."""
    for index in range(11):
        _create_product_through_api(client, f"Item {index}")

    response = client.get("/web/inventory/list")

    assert response.status_code == httpx.codes.OK
    assert "Load more" in response.text


def test_inventory_soon_page_renders_urgency_screen(client: TestClient) -> None:
    """The urgency route should render the dedicated soon screen shell."""
    response = client.get("/web/inventory/soon")

    assert response.status_code == httpx.codes.OK
    assert "Expiring soon" in response.text
    assert "Soon" in response.text


def test_more_page_renders_utility_screen(client: TestClient) -> None:
    """The More destination should render utility links instead of jumping straight to docs."""
    response = client.get("/web/more")

    assert response.status_code == httpx.codes.OK
    assert "Tools" in response.text
    assert "API documentation" in response.text


def test_new_product_page_renders_form(client: TestClient) -> None:
    """The add-product page should render the shared product form."""
    response = client.get("/web/inventory/new")

    assert response.status_code == httpx.codes.OK
    assert "Create product" in response.text
    assert 'name="product_name"' in response.text
    assert 'type="date"' in response.text
    assert 'type="time"' not in response.text


def test_create_product_page_creates_product_and_shows_flash(client: TestClient) -> None:
    """Submitting the add form should create a product and redirect back home."""
    response = client.post("/web/inventory", data=_html_form_payload(product_name="Ricotta"))

    assert response.status_code == httpx.codes.OK
    assert "Product created successfully" in response.text
    assert "Ricotta" in response.text
    assert "Open inventory" in response.text


def test_create_product_page_allows_empty_description(client: TestClient) -> None:
    """Description should be optional in the web form."""
    response = client.post(
        "/web/inventory", data=_html_form_payload(product_name="Ricotta", description="")
    )

    assert response.status_code == httpx.codes.OK
    assert "Product created successfully" in response.text
    assert "Ricotta" in response.text


def test_inventory_page_uses_user_facing_units_and_dates(client: TestClient) -> None:
    """The inventory page should show human-readable units and date-only expiry values."""
    client.post("/web/inventory", data=_html_form_payload(product_name="Ricotta"))

    response = client.get("/web/inventory")

    assert response.status_code == httpx.codes.OK
    assert "2 boxes" in response.text
    assert "ProductUnitEnum" not in response.text


def test_create_product_page_rerenders_errors(client: TestClient) -> None:
    """Invalid form data should rerender the add page with inline validation errors."""
    response = client.post("/web/inventory", data=_html_form_payload(quantity="0"))

    assert response.status_code == httpx.codes.OK
    assert "greater than or equal to 1" in response.text
    assert "Create product" in response.text


def test_create_product_page_handles_missing_expiry_field(client: TestClient) -> None:
    """Missing form fields should rerender the page instead of returning a JSON 422."""
    payload = _html_form_payload()
    payload.pop("expiry_date_date")

    response = client.post("/web/inventory", data=payload)

    assert response.status_code == httpx.codes.OK
    assert "Field required" in response.text
    assert "Create product" in response.text


def test_edit_product_page_renders_existing_values(client: TestClient) -> None:
    """Editing an existing product should prefill the form fields."""
    product_id = _create_product_through_api(client, "Blueberries")

    response = client.get(f"/web/inventory/{product_id}/edit")

    assert response.status_code == httpx.codes.OK
    assert "Edit Blueberries" in response.text
    assert 'value="Blueberries"' in response.text
    assert 'type="time"' not in response.text


def test_update_product_page_persists_changes(client: TestClient) -> None:
    """Submitting the edit form should update the product and return home with a flash."""
    product_id = _create_product_through_api(client, "Cottage Cheese")
    response = client.post(
        f"/web/inventory/{product_id}",
        data=_html_form_payload(product_name="Skyr", description="Icelandic dairy"),
    )

    assert response.status_code == httpx.codes.OK
    assert "Product updated successfully" in response.text
    assert "Skyr" in response.text
    assert "Cottage Cheese" not in response.text


def test_delete_product_page_removes_product(client: TestClient) -> None:
    """Deleting from the HTML UI should remove the product and redirect home."""
    product_id = _create_product_through_api(client, "Parsley")

    response = client.post(f"/web/inventory/{product_id}/delete")

    assert response.status_code == httpx.codes.OK
    assert "Product deleted successfully" in response.text
    assert "Parsley" not in response.text
