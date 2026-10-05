import pytest
from playwright.sync_api import expect


@pytest.mark.smoke
def test_add_single_item_to_cart(inventory_page, cart_page):
    inventory_page.add_to_cart("sauce-labs-backpack")
    expect(inventory_page.cart_badge).to_have_text("1")

    inventory_page.open_cart()
    expect(cart_page.items).to_have_count(1)
    expect(cart_page.item_names).to_have_text("Sauce Labs Backpack")


def test_add_multiple_items_updates_badge(inventory_page):
    inventory_page.add_to_cart("sauce-labs-backpack")
    inventory_page.add_to_cart("sauce-labs-bike-light")
    expect(inventory_page.cart_badge).to_have_text("2")


def test_remove_item_clears_badge(inventory_page):
    inventory_page.add_to_cart("sauce-labs-backpack")
    inventory_page.remove_from_cart("sauce-labs-backpack")
    expect(inventory_page.cart_badge).to_have_count(0)
