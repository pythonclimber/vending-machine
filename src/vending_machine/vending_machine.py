from dataclasses import dataclass
from typing import Tuple


@dataclass
class Item:
    price: float
    name: str


class VendingMachine:
    def __init__(self):
        self.current_payment = 0.00
        self.items = {
            'A1': [Item(0.75, 'Chips')] * 10,
            'A2': [Item(0.65, 'Pretzels')] * 10,
            'B1': [Item(0.85, 'Cookies')] * 10
        }

    def get_price(self, position_code) -> float:
        return self.items[position_code][0].price

    def insert_payment(self, payment: float):
        self.current_payment = payment

    def refund_payment(self):
        amount_to_refund = self.current_payment
        self.current_payment = 0.00
        return amount_to_refund

    def dispense_item_with_change(self, position_code) -> Tuple[Item, float]:
        if position_code not in self.items:
            raise ValueError('Invalid position')

        if not self.items[position_code]:
            raise ValueError('Item out of stock')

        if self.current_payment < self.items[position_code][0].price:
            raise ValueError('Insufficient funds provided')

        item = self.items[position_code].pop()
        change = self.current_payment - item.price
        self.current_payment = 0.00

        return item, change

