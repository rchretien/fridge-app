"""CRUD operations for product location model."""

from fridge_app_backend.orm.crud.base_crud import CRUDBase
from fridge_app_backend.orm.models.db_models import ProductType
from fridge_app_backend.orm.schemas.product_type_schemas import ProductTypeCreate, ProductTypeUpdate


class CRUDProductType(CRUDBase[ProductType, ProductTypeCreate, ProductTypeUpdate]):
    """CRUD operations for product location model."""


product_type_crud = CRUDProductType(ProductType)
