from typing import Dict
from src.models import Product, Offer
from src.handlers.receipt import Receipt
from src.handlers.discount_calculator import IDiscountStrategyFactory
from src.handlers.catalog import ISupermarketCatalog


class ShoppingCart:
    """Handles the management of products added to the cart."""

    def __init__(self):
        self._product_quantities: Dict[Product, float] = {}

    def add_item(self, product: Product) -> None:
        """Adds a single unit of a product to the cart."""
        self.add_item_quantity(product, 1.0)

    def add_item_quantity(self, product: Product, quantity: float) -> None:
        """Adds a specified quantity of a product to the cart."""
        if product in self._product_quantities:
            self._product_quantities[product] += quantity
        else:
            self._product_quantities[product] = quantity

    def handle_offers(
        self, receipt: Receipt, offers: Dict[Product, Offer], catalog: ISupermarketCatalog
    ) -> None:
        """Applies applicable offers to the products in the cart."""
        for product, quantity in self._product_quantities.items():
            if product in offers:
                offer = offers[product]
                unit_price = catalog.unit_price(product)
                strategy = IDiscountStrategyFactory.get_strategy(offer.offer_type)
                discount = strategy.calculate(product, quantity, offer, unit_price)
                if discount:
                    receipt.add_discount(discount)