from abc import ABC, abstractmethod
from src.models import Discount, Product, SpecialOfferType, Offer
from typing import Optional


class IDiscountStrategy(ABC):
    """Abstract base class for discount calculation strategies."""

    @abstractmethod
    def calculate(
        self, product: Product, quantity: float, offer: Offer, unit_price: float
    ) -> Optional[Discount]:
        pass


class ThreeForTwoStrategy(IDiscountStrategy):
    def calculate(
        self, product: Product, quantity: float, offer: Offer, unit_price: float
    ) -> Optional[Discount]:
        """Calculates a 'Three for Two' discount."""
        num_free = int(quantity // 3)
        discount_amount = num_free * unit_price
        return Discount(product, "3 for 2", -discount_amount) if discount_amount > 0 else None


class TenPercentDiscountStrategy(IDiscountStrategy):
    def calculate(
        self, product: Product, quantity: float, offer: Offer, unit_price: float
    ) -> Optional[Discount]:
        """Calculates a 10% discount."""
        discount_amount = quantity * unit_price * (offer.argument / 100.0)
        return Discount(product, f"{offer.argument}% off", -discount_amount) if discount_amount > 0 else None
    

class TwoForAmountStrategy(IDiscountStrategy):
    def calculate(
        self, product: Product, quantity: float, offer: Offer, unit_price: float
    ) -> Optional[Discount]:
        """Calculates a 'Two for Amount' discount."""
        num_offers = int(quantity // 2)
        discount_amount = num_offers * (2 * unit_price - offer.argument)
        return Discount(product, f"2 for {offer.argument}", -discount_amount) if discount_amount > 0 else None


class FiveForAmountStrategy(IDiscountStrategy):
    def calculate(
        self, product: Product, quantity: float, offer: Offer, unit_price: float
    ) -> Optional[Discount]:
        """Calculates a 'Five for Amount' discount."""
        num_offers = int(quantity // 5)
        discount_amount = num_offers * (5 * unit_price - offer.argument)
        return Discount(product, f"5 for {offer.argument}", -discount_amount) if discount_amount > 0 else None


class IDiscountStrategyFactory:
    """Factory class for creating discount strategy instances."""

    @staticmethod
    def get_strategy(offer_type: SpecialOfferType) -> IDiscountStrategy:
        """Returns the appropriate strategy for the given offer type."""

        if offer_type == SpecialOfferType.THREE_FOR_TWO:
            return ThreeForTwoStrategy()
        if offer_type == SpecialOfferType.PERCENT_DISCOUNT:
            return TenPercentDiscountStrategy()
        if offer_type == SpecialOfferType.TWO_FOR_AMOUNT:
            return TwoForAmountStrategy()
        if offer_type == SpecialOfferType.FIVE_FOR_AMOUNT:
            return FiveForAmountStrategy()
        raise ValueError(f"No strategy found for offer type: {offer_type}")