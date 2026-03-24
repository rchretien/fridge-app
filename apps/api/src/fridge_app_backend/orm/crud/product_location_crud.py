"""CRUD operations for the product location model."""

from fridge_app_backend.orm.crud.base_crud import CRUDBase
from fridge_app_backend.orm.models.db_models import ProductLocation
from fridge_app_backend.orm.schemas.product_location_schemas import (
    ProductLocationCreate,
    ProductLocationUpdate,
)


class CRUDProductLocation(CRUDBase[ProductLocation, ProductLocationCreate, ProductLocationUpdate]):
    """CRUD operations for product location model."""


product_location_crud = CRUDProductLocation(ProductLocation)
