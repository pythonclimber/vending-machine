from src.vending_machine.vending_machine import VendingMachine, Item
from pytest import fixture, raises


@fixture
def vending_machine():
    return VendingMachine()


def test_vending_machine_has_10_chips(vending_machine):
    position_code = 'A1'
    assert vending_machine.items[position_code][0].name == 'Chips'
    assert len(vending_machine.items[position_code]) == 10


def test_vending_machine_has_10_pretzels(vending_machine):
    position_code = 'A2'
    assert vending_machine.items[position_code][0].name == 'Pretzels'
    assert len(vending_machine.items[position_code]) == 10


def test_vending_machine_has_10_cookies(vending_machine):
    position_code = 'B1'
    assert vending_machine.items[position_code][0].name == 'Cookies'
    assert len(vending_machine.items[position_code]) == 10


def test_chips_cost_seventy_five_cents(vending_machine):
    chips_position = 'A1'
    assert vending_machine.get_price(chips_position) == 0.75


def test_pretzels_cost_sixty_five_cents(vending_machine):
    pretzels_position = 'A2'
    assert vending_machine.get_price(pretzels_position) == 0.65


def test_cookies_cost_eighty_five_cents(vending_machine):
    cookies_position = 'B1'
    assert vending_machine.get_price(cookies_position) == 0.85
    

def test_insert_payment(vending_machine):
    payment_amount = 1.00
    vending_machine.insert_payment(payment_amount)
    assert vending_machine.current_payment == payment_amount


def test_refund_payment(vending_machine):
    payment_amount = 0.50
    vending_machine.insert_payment(payment_amount)
    refund_amount = vending_machine.refund_payment()
    assert refund_amount == payment_amount
    assert vending_machine.current_payment == 0.00


def test_dispense_invalid_item(vending_machine):
    position_code = 'C1'
    with raises(ValueError) as ex:
        vending_machine.dispense_item_with_change(position_code)
    assert 'Invalid position' in str(ex)


def test_dispense_insufficient_funds(vending_machine):
    position_code = 'A1'
    vending_machine.insert_payment(0.50)
    with raises(ValueError) as ex:
        vending_machine.dispense_item_with_change(position_code)
    assert 'Insufficient funds provided' in str(ex)


def test_dispense_item_out_of_stock(vending_machine):
    position_code = 'B1'
    vending_machine.items[position_code] = []
    vending_machine.insert_payment(0.85)
    with raises(ValueError) as ex:
        vending_machine.dispense_item_with_change(position_code)
    assert 'Item out of stock' in str(ex)


def test_dispense_with_exact_amount(vending_machine):
    position_code = 'A2'
    vending_machine.insert_payment(0.65)
    item, change = vending_machine.dispense_item_with_change(position_code)
    assert item.name == 'Pretzels'
    assert change == 0.00


def test_dispense_payment_is_cleared(vending_machine):
    position_code = 'A1'
    vending_machine.insert_payment(0.75)
    vending_machine.dispense_item_with_change(position_code)
    assert vending_machine.current_payment == 0.00


def test_dispense_quantity_is_updated(vending_machine):
    position_code = 'A1'
    vending_machine.insert_payment(0.75)
    vending_machine.dispense_item_with_change(position_code)
    assert len(vending_machine.items[position_code]) == 9


def test_dispense_with_over_payment(vending_machine):
    position_code = 'A1'
    vending_machine.insert_payment(1.00)
    _, change = vending_machine.dispense_item_with_change(position_code)
    assert change == 0.25

