from typing import Dict
import pytest
from src.models import Product
from src.handlers.shopping_cart import ShoppingCart
from src.handlers.teller import Teller


class TestFailCases:
    """Tests for invalid inputs and fail cases."""

    @pytest.mark.xfail
    def test_invalid_product(
        self, teller: Teller, catalog, cart: ShoppingCart
    ):
        """Ensure an error is raised for an invalid product."""
        invalid_product = Product("invalid", "unknown")

        cart.add_item_quantity(invalid_product, 1)

        with pytest.raises(KeyError):
            teller.checks_out_articles_from(cart)