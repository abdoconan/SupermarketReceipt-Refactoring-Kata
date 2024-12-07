from typing import List
from src.models import ReceiptItem, Discount, Product




class Receipt:
    def __init__(self):
        self._items: List[ReceiptItem] = []
        self._discounts: List[Discount] = []

    def total_price(self):
        total = 0
        for item in self.items:
            total += item.total_price
        for discount in self.discounts:
            total += discount.discount_amount
        return total

    def add_product(self, product: Product, quantity: int, price: float, total_price: float):
        self._items.append(ReceiptItem(product, quantity, price, total_price))

    def add_discount(self, discount: Discount):
        self._discounts.append(discount)

    @property
    def items(self):
        return self._items[:]

    @property
    def discounts(self):
        return self._discounts[:]
