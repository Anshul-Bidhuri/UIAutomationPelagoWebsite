from Pages.basepage import BasePage
from Helpers import driver_helpers, custom_logger
import locators

log = custom_logger.get_logger()


class ActivityPage(BasePage):

    def click_first_active_date(self):
        driver_helpers.click_element(self.driver, locators.first_active_date_xpath)

    def click_select_activity_button(self):
        driver_helpers.click_element(self.driver, locators.button_select_activity_xpath, timeout=10)

    def get_activity_price(self):
        price = driver_helpers.get_text_from_element(self.driver, locators.activity_footer_price_xpath)
        log.info(f"Activity price: {price}")
        return price

    def click_add_activity_to_cart_button(self):
        driver_helpers.click_element(self.driver, locators.button_add_activity_to_cart_xpath, timeout=10)

    def click_view_cart_button(self):
        driver_helpers.click_element(self.driver, locators.button_view_cart_notification_xpath, timeout=10)
