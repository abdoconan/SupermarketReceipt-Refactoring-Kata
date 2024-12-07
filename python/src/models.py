from typing import Optional
from src.enums import ProductUnit, SpecialOfferType

class Product:
    def __init__(self, name: str, unit: ProductUnit):
        self.name: str = name
        self.unit: ProductUnit = unit


class ProductQuantity:
    def __init__(self, product: Product, quantity: int):
        self.product: Product = product
        self.quantity: int = quantity

class Offer:
    def __init__(self, offer_type: SpecialOfferType, product: Product, argument: Optional[float] = None):
        self.offer_type: SpecialOfferType = offer_type
        self.product: Product = product
        self.argument: Optional[float] = argument


class Discount:
    def __init__(self, product: Product, description: str, discount_amount: float):
        self.product: Product = product
        self.description: str = description
        self.discount_amount: float = discount_amount


class ReceiptItem:
    def __init__(self, product: Product, quantity: int, price: float, total_price: float):
        self.product: Product = product
        self.quantity: int = quantity
        self.price: float = price
        self.total_price: float = total_price