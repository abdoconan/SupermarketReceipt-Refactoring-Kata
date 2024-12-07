from src.models import Product, SpecialOfferType, ProductUnit
from src.handlers.catalog import CatalogFactory, ISupermarketCatalog
from src.handlers.shopping_cart import ShoppingCart
from src.handlers.teller import Teller
from src.handlers.receipt_printer import ReceiptPrinter

catalog: ISupermarketCatalog = CatalogFactory().create_catalog(is_testing=True)
teller: Teller = Teller(catalog)

toothbrush = Product("toothbrush", ProductUnit.EACH)
apples = Product("apples", ProductUnit.KILO)
rice = Product("rice", ProductUnit.EACH)
toothpaste = Product("toothpaste", ProductUnit.EACH)
tomatoes = Product("cherry tomatoes", ProductUnit.EACH)

catalog.add_product(toothbrush, 0.99)
catalog.add_product(apples, 1.99)
catalog.add_product(rice, 2.49)
catalog.add_product(toothpaste, 1.79)
catalog.add_product(tomatoes, 0.69)

products =  {
    "toothbrush": toothbrush,
    "apples": apples,
    "rice": rice,
    "toothpaste": toothpaste,
    "tomatoes": tomatoes,
}

cart : ShoppingCart =  ShoppingCart()

teller.add_special_offer(SpecialOfferType.PERCENT_DISCOUNT, apples, 20.0)
teller.add_special_offer(SpecialOfferType.FIVE_FOR_AMOUNT, toothpaste, 7.49)

cart.add_item_quantity(apples, 3)
cart.add_item_quantity(toothpaste, 5)

receipt = teller.checks_out_articles_from(cart)

receipt_printer: ReceiptPrinter = ReceiptPrinter()
print(receipt_printer.print_receipt(receipt))
