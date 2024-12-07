import pytest
from typing import Dict
from src.models import Product, SpecialOfferType
from src.handlers.shopping_cart import ShoppingCart
from src.handlers.teller import Teller


class TestDiscounts:
    """Tests for validating various discount scenarios."""

    def test_three_for_two_discount(
        self, teller: Teller, products: Dict[str, Product], cart: ShoppingCart
    ):
        """
        Validate the '3 for 2' discount on toothbrushes.
        Normal toothbrush price is €0.99.
        """
        toothbrush = products["toothbrush"]
        teller.add_special_offer(SpecialOfferType.THREE_FOR_TWO, toothbrush, None)
        cart.add_item_quantity(toothbrush, 3)

        receipt = teller.checks_out_articles_from(cart)

        assert receipt.total_price() == pytest.approx(1.98, 0.01)
        assert len(receipt.discounts) == 1
        discount = receipt.discounts[0]
        assert discount.product == toothbrush
        assert discount.description == "3 for 2"
        assert discount.discount_amount == pytest.approx(-0.99, 0.01)

    def test_twenty_percent_discount_on_apples(
        self, teller: Teller, products: Dict[str, Product], cart: ShoppingCart
    ):
        """
        Validate the 20% discount on apples.
        Normal apple price is €1.99 per kilo.
        """
        apples = products["apples"]
        teller.add_special_offer(SpecialOfferType.PERCENT_DISCOUNT, apples, 20.0)
        cart.add_item_quantity(apples, 2)

        receipt = teller.checks_out_articles_from(cart)

        assert receipt.total_price() == pytest.approx(3.184, 0.01)
        assert len(receipt.discounts) == 1
        discount = receipt.discounts[0]
        assert discount.product == apples
        assert discount.description == "20.0% off"
        assert discount.discount_amount == pytest.approx(-0.796, 0.01)

    def test_ten_percent_discount_on_rice(
        self, teller: Teller, products: Dict[str, Product], cart: ShoppingCart
    ):
        """
        Validate the 10% discount on rice.
        Normal rice price is €2.49 per bag.
        """
        rice = products["rice"]
        teller.add_special_offer(SpecialOfferType.PERCENT_DISCOUNT, rice, 10.0)
        cart.add_item_quantity(rice, 1)

        receipt = teller.checks_out_articles_from(cart)

        assert receipt.total_price() == pytest.approx(2.24, 0.01)
        assert len(receipt.discounts) == 1
        discount = receipt.discounts[0]
        assert discount.product == rice
        assert discount.description == "10.0% off"
        assert discount.discount_amount == pytest.approx(-0.25, 0.01)

    def test_five_for_specific_price_toothpaste(
        self, teller: Teller, products: Dict[str, Product], cart: ShoppingCart
    ):
        """
        Validate the '5 for €7.49' discount on toothpaste.
        Normal toothpaste price is €1.79.
        """
        toothpaste = products["toothpaste"]
        teller.add_special_offer(SpecialOfferType.FIVE_FOR_AMOUNT, toothpaste, 7.49)
        cart.add_item_quantity(toothpaste, 5)

        receipt = teller.checks_out_articles_from(cart)

        assert receipt.total_price() == pytest.approx(7.49, 0.01)
        assert len(receipt.discounts) == 1
        discount = receipt.discounts[0]
        assert discount.product == toothpaste
        assert discount.description == "5 for 7.49"
        assert discount.discount_amount == pytest.approx(-1.46, 0.01)

    def test_two_for_specific_price_tomatoes(
        self, teller: Teller, products: Dict[str, Product], cart: ShoppingCart
    ):
        """
        Validate the '2 for €0.99' discount on cherry tomatoes.
        Normal tomato price is €0.69 per box.
        """
        tomatoes = products["tomatoes"]
        teller.add_special_offer(SpecialOfferType.TWO_FOR_AMOUNT, tomatoes, 0.99)
        cart.add_item_quantity(tomatoes, 2)

        receipt = teller.checks_out_articles_from(cart)

        assert receipt.total_price() == pytest.approx(0.99, 0.01)
        assert len(receipt.discounts) == 1
        discount = receipt.discounts[0]
        assert discount.product == tomatoes
        assert discount.description == "2 for 0.99"
        assert discount.discount_amount == pytest.approx(-0.39, 0.01)

    def test_no_discount_for_extra_items(
        self, teller: Teller, products: Dict[str, Product], cart: ShoppingCart
    ):
        """
        Validate that no discount is applied for extra items not meeting the deal requirements.
        For example, 4 tubes of toothpaste under a '5 for €7.49' deal.
        """
        toothpaste = products["toothpaste"]
        teller.add_special_offer(SpecialOfferType.FIVE_FOR_AMOUNT, toothpaste, 7.49)
        cart.add_item_quantity(toothpaste, 4)

        receipt = teller.checks_out_articles_from(cart)

        assert receipt.total_price() == pytest.approx(4 * 1.79, 0.01)
        assert len(receipt.discounts) == 0

    def test_combined_discounts(
        self, teller: Teller, products: Dict[str, Product], cart: ShoppingCart
    ):
        """
        Validate a cart with multiple discounts applied.
        Apples with 20% off and toothpaste with '5 for €7.49'.
        """
        apples = products["apples"]
        toothpaste = products["toothpaste"]

        teller.add_special_offer(SpecialOfferType.PERCENT_DISCOUNT, apples, 20.0)
        teller.add_special_offer(SpecialOfferType.FIVE_FOR_AMOUNT, toothpaste, 7.49)

        cart.add_item_quantity(apples, 3)
        cart.add_item_quantity(toothpaste, 5)

        receipt = teller.checks_out_articles_from(cart)

        # Validate total price
        apples_discount = 3 * 1.99 * 0.2
        toothpaste_discount = (5 * 1.79) - 7.49
        total_discount = apples_discount + toothpaste_discount
        expected_total = (3 * 1.99 + 5 * 1.79) - total_discount
        assert receipt.total_price() == pytest.approx(expected_total, 0.01)

        # Validate discounts
        assert len(receipt.discounts) == 2
