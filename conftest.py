import json
from pathlib import Path

import pytest

from pages.cart_page import CartPage
from pages.inventory_page import InventoryPage
from pages.login_page import LoginPage

USERS_FILE = Path(__file__).parent / "test_data" / "users.json"


@pytest.fixture(scope="session")
def users():
    return json.loads(USERS_FILE.read_text())


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
