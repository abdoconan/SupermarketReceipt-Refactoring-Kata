from src.models import ReceiptItem, Discount
from src.handlers.receipt import Receipt

class ReceiptPrinter:
    """Generates a printable receipt."""

    def __init__(self, columns: int = 40):
        self.columns = columns

    def print_receipt(self, receipt: Receipt) -> str:
        """Generates a receipt string."""
        result = ""
        for item in receipt.items:
            result += self.print_receipt_item(item)

        for discount in receipt.discounts:
            result += self.print_discount(discount)

        result += "\n" + self.present_total(receipt)
        return result

    def print_receipt_item(self, item: ReceiptItem) -> str:
        """Prints a receipt item."""
        total_price = self.format_price(item.total_price)
        line = self.format_line(item.product.name, total_price)
        if item.quantity != 1:
            line += f"  {self.format_price(item.price)} * {item.quantity}\n"
        return line

    def print_discount(self, discount: Discount) -> str:
        """Prints a discount."""
        name = f"{discount.description} ({discount.product.name})"
        value = self.format_price(discount.discount_amount)
        return self.format_line(name, value)

    def present_total(self, receipt: Receipt) -> str:
        """Prints the total price."""
        name = "Total: "
        value = self.format_price(receipt.total_price())
        return self.format_line(name, value)

    def format_price(self, price: float) -> str:
        """Formats a price as a string."""
        return f"{price:.2f}"

    def format_line(self, name: str, value: str) -> str:
        """Formats a line with whitespace."""
        whitespace = " " * (self.columns - len(name) - len(value))
        return f"{name}{whitespace}{value}\n"