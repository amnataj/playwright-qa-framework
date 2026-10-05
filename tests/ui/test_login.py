import pytest
from playwright.sync_api import expect

from pages.inventory_page import InventoryPage


@pytest.mark.smoke
def test_valid_login(page, login_page, users):
    login_page.login(**users["standard"])
    inventory = InventoryPage(page)
    expect(page).to_have_url("/inventory.html")
    expect(inventory.title).to_have_text("Products")


@pytest.mark.negative
def test_locked_out_user(login_page, users):
    login_page.login(**users["locked_out"])
    expect(login_page.error_message).to_contain_text("locked out")


@pytest.mark.negative
@pytest.mark.parametrize(
    "username, password, expected_error",
    [
        ("", "secret_sauce", "Username is required"),
        ("standard_user", "", "Password is required"),
        ("standard_user", "wrong_pass", "do not match any user"),
        ("not_a_user", "secret_sauce", "do not match any user"),
    ],
    ids=["no-username", "no-password", "wrong-password", "unknown-user"],
)
def test_invalid_login(login_page, username, password, expected_error):
    login_page.login(username, password)
    expect(login_page.error_message).to_contain_text(expected_error)
