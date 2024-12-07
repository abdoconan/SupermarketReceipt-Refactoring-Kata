from typing import Dict, Optional
from src.models import Offer, Product
from src.handlers.receipt import Receipt
from src.handlers.catalog import ISupermarketCatalog
from src.handlers.shopping_cart import ShoppingCart
from src.enums import SpecialOfferType


class Teller:
    """Handles the checkout process."""

    def __init__(self, catalog: ISupermarketCatalog):
        self.catalog = catalog
        self.offers: Dict[Product, Offer] = {}

    def add_special_offer(
        self, offer_type: SpecialOfferType, product: Product, argument: Optional[float] = None
    ) -> None:
        """Adds a special offer to the teller."""
        self.offers[product] = Offer(offer_type, product, argument)

    def checks_out_articles_from(self, the_cart: ShoppingCart) -> Receipt:
        """Processes a shopping cart and generates a receipt."""
        receipt: Receipt = Receipt()
        for product, quantity in the_cart._product_quantities.items():
            unit_price = self.catalog.unit_price(product)
            total_price = quantity * unit_price
            receipt.add_product(product, quantity, unit_price, total_price)

        the_cart.handle_offers(receipt, self.offers, self.catalog)
        return receipt