import pytest
from src.models import Product, ProductUnit
from src.handlers.teller import Teller
from src.handlers.shopping_cart import ShoppingCart
from src.handlers.catalog import CatalogFactory, ISupermarketCatalog


@pytest.fixture
def catalog() -> ISupermarketCatalog:
    """Fixture for an in-memory catalog."""
    return CatalogFactory().create_catalog(is_testing=True)


@pytest.fixture
def teller(catalog: ISupermarketCatalog) -> Teller:
    """Fixture for the teller."""
    return Teller(catalog)


@pytest.fixture
def products(catalog: ISupermarketCatalog) -> dict:
    """Fixture for adding common products to the catalog."""
    toothbrush = Product("toothbrush", ProductUnit.EACH)
    apples = Product("apples", ProductUnit.KILO)
    rice = Product("rice", ProductUnit.EACH)
    toothpaste = Product("toothpaste", ProductUnit.EACH)
    tomatoes = Product("cherry tomatoes", ProductUnit.EACH)

    catalog.add_product(toothbrush, 0.99)
    catalog.add_product(apples, 1.99)
    catalog.add_product(rice, 2.49)
    catalog.add_product(toothpaste, 1.79)
    catalog.add_product(tomatoes, 0.69)

    return {
        "toothbrush": toothbrush,
        "apples": apples,
        "rice": rice,
        "toothpaste": toothpaste,
        "tomatoes": tomatoes,
    }


@pytest.fixture
def cart() -> ShoppingCart:
    """Fixture for a shopping cart."""
    return ShoppingCart()