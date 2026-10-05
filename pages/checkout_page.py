import re

from playwright.sync_api import Locator, Page
from pages.base_page import BasePage


class CheckoutPage(BasePage):
    """Covers the three checkout screens: information, overview, complete."""

    def __init__(self, page: Page):
        super().__init__(page)
        # Step one: customer information
        self.first_name = page.locator('[data-test="firstName"]')
        self.last_name = page.locator('[data-test="lastName"]')
        self.postal_code = page.locator('[data-test="postalCode"]')
        self.continue_button = page.locator('[data-test="continue"]')
        self.error_message = page.locator('[data-test="error"]')
        # Step two: overview
        self.items = page.locator('[data-test="inventory-item"]')
        self.subtotal_label = page.locator('[data-test="subtotal-label"]')
        self.tax_label = page.locator('[data-test="tax-label"]')
        self.total_label = page.locator('[data-test="total-label"]')
        self.finish_button = page.locator('[data-test="finish"]')
        # Step three: complete
        self.complete_header = page.locator('[data-test="complete-header"]')

    def fill_information(self, first_name: str, last_name: str, postal_code: str):
        self.first_name.fill(first_name)
        self.last_name.fill(last_name)
        self.postal_code.fill(postal_code)
        self.continue_button.click()

    def finish(self):
        self.finish_button.click()

    @staticmethod
    def amount(label: Locator) -> float:
        """Extract the dollar amount from text like 'Item total: $29.99'."""
        match = re.search(r"\$(\d+\.\d{2})", label.inner_text())
        assert match, f"No dollar amount found in label: {label.inner_text()!r}"
        return float(match.group(1))
