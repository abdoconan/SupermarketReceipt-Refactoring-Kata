import pytest
from typing import Dict
from src.models import Product, SpecialOfferType
from src.handlers.shopping_cart import ShoppingCart
from src.handlers.teller import Teller


class TestEdgeCases:
    """Tests for validating edge case scenarios."""

    def test_no_discount_for_insufficient_items(
        self, teller: Teller, products: Dict[str, Product], cart: ShoppingCart
    ):
        """Ensure no discount is applied when required items are not met."""
        toothbrush = products["toothbrush"]
        teller.add_special_offer(SpecialOfferType.THREE_FOR_TWO, toothbrush, None)
        cart.add_item_quantity(toothbrush, 2)

        receipt = teller.checks_out_articles_from(cart)

        assert receipt.total_price() == pytest.approx(1.98, 0.01)
        assert len(receipt.discounts) == 0