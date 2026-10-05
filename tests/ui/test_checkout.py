import pytest
from playwright.sync_api import expect


@pytest.mark.smoke
def test_successful_checkout(page, checkout_ready, customer):
    checkout_ready.fill_information(**customer)
    expect(page).to_have_url("/checkout-step-two.html")

    checkout_ready.finish()
    expect(page).to_have_url("/checkout-complete.html")
    expect(checkout_ready.complete_header).to_have_text("Thank you for your order!")


@pytest.mark.negative
@pytest.mark.parametrize(
    "first_name, last_name, postal_code, expected_error",
    [
        ("", "User", "44000", "First Name is required"),
        ("Test", "", "44000", "Last Name is required"),
        ("Test", "User", "", "Postal Code is required"),
    ],
    ids=["no-first-name", "no-last-name", "no-postal-code"],
)
def test_checkout_requires_all_fields(
    page, checkout_ready, first_name, last_name, postal_code, expected_error
):
    checkout_ready.fill_information(first_name, last_name, postal_code)
    expect(checkout_ready.error_message).to_contain_text(expected_error)
    expect(page).to_have_url("/checkout-step-one.html")


def test_order_total_is_subtotal_plus_tax(checkout_ready, customer):
    checkout_ready.fill_information(**customer)
    subtotal = checkout_ready.amount(checkout_ready.subtotal_label)
    tax = checkout_ready.amount(checkout_ready.tax_label)
    total = checkout_ready.amount(checkout_ready.total_label)
    assert round(subtotal + tax, 2) == total


def test_overview_lists_all_cart_items(
    inventory_page, cart_page, checkout_page, customer
):
    inventory_page.add_to_cart("sauce-labs-backpack")
    inventory_page.add_to_cart("sauce-labs-bike-light")
    inventory_page.open_cart()
    cart_page.proceed_to_checkout()
    checkout_page.fill_information(**customer)

    expect(checkout_page.items).to_have_count(2)
    subtotal = checkout_page.amount(checkout_page.subtotal_label)
    assert subtotal == pytest.approx(29.99 + 9.99)
