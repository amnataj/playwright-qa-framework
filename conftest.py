import os
import json
from pathlib import Path
import pytest

from pages.cart_page import CartPage
from pages.checkout_page import CheckoutPage
from pages.inventory_page import InventoryPage
from pages.login_page import LoginPage

DATA_DIR = Path(__file__).parent / "test_data"


def _load(name: str) -> dict:
    return json.loads((DATA_DIR / name).read_text())

@pytest.fixture(scope="session")
def base_url():
    return os.getenv("BASE_URL", "https://www.saucedemo.com")

@pytest.fixture(scope="session")
def users():
    return _load("users.json")


@pytest.fixture(scope="session")
def customer():
    return _load("customer.json")


@pytest.fixture
def login_page(page):
    lp = LoginPage(page)
    lp.load()
    return lp


@pytest.fixture
def inventory_page(page, login_page, users):
    """Logs in as the standard user and returns the inventory page."""
    login_page.login(**users["standard"])
    return InventoryPage(page)


@pytest.fixture
def cart_page(page):
    return CartPage(page)


@pytest.fixture
def checkout_page(page):
    return CheckoutPage(page)


@pytest.fixture
def checkout_ready(inventory_page, cart_page, checkout_page):
    """Logged in, one backpack in the cart, sitting on checkout step one."""
    inventory_page.add_to_cart("sauce-labs-backpack")
    inventory_page.open_cart()
    cart_page.proceed_to_checkout()
    return checkout_page
