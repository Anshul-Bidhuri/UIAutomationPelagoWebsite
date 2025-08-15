# import sys, os
# main_project_path = os.path.abspath(__file__+"../../../")
# sys.path.append(main_project_path)

from Pages.basepage import BasePage
from Helpers import driver_helpers, custom_logger
import locators

log = custom_logger.get_logger()


class CartPage(BasePage):
    """
    Page object class for handling interactions with the Cart page.
    """

    def check_empty_cart_message_visibility(self):
        """
        Checks if the empty cart message is visible on the page.
        
        Returns:
            bool: True if empty cart message is visible, False otherwise.
        """
        element = driver_helpers.wait_till_element_is_visible(self.driver, locators.empty_cart_text_xpath)
        if element.is_displayed():
            log.info("Empty cart message is visible")
            return True
        else:
            log.error("Empty cart message is not visible")
            return False

    def click_explore_activities_button(self):
        """
        Clicks the explore activities button on the cart page.
        
        Returns:
            None
        """
        driver_helpers.click_element(self.driver, locators.button_explore_activities_xpath, timeout=10)

    def get_price_of_cart_item(self):
        """
        Retrieves the price of an item in the cart.
        
        Returns:
            str: The price of the cart item as displayed on the page.
        """
        price = driver_helpers.get_text_from_element(self.driver, locators.price_per_cart_item_xpath)
        log.info(f"Cart item price: {price}")
        return price

