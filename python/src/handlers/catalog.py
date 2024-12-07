from abc import ABC, abstractmethod
from typing import Dict
from src.models import Product


class ISupermarketCatalog(ABC):
    """Abstract base class for catalog operations."""

    @abstractmethod
    def add_product(self, product: Product, price: float) -> None:
        pass

    @abstractmethod
    def unit_price(self, product: Product) -> float:
        pass

class SupermarketCatalog(ISupermarketCatalog):

    def add_product(self, product: Product, price: float) -> None:
        raise Exception("cannot be called from a unit test - it accesses the database")

    def unit_price(self, product: Product) -> float:
        raise Exception("cannot be called from a unit test - it accesses the database")



class InMemoryCatalog(ISupermarketCatalog):
    """Concrete implementation of ISupermarketCatalog for in-memory storage."""

    def __init__(self):
        self.products: Dict[Product, float] = {}

    def add_product(self, product: Product, price: float) -> None:
        self.products[product] = price

    def unit_price(self, product: Product) -> float:
        return self.products.get(product, 0.0)
    

class CatalogFactory:
    """Factory class for creating catalog instances."""

    @staticmethod
    def create_catalog(is_testing: bool = False) -> ISupermarketCatalog:
        """Creates and returns an in-memory catalog."""
        if is_testing:
            return InMemoryCatalog()
        
        return SupermarketCatalog()