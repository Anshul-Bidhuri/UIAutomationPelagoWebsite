from Pages.basepage import BasePage
from Helpers import driver_helpers, custom_logger
import locators

log = custom_logger.get_logger()


class ActivityPage(BasePage):
    """
    Page object class for handling interactions with the Activity page.
    """

    def click_first_active_date(self):
        """
        Clicks on the first available active date for the activity.
        
        Returns:
            None
        """
        driver_helpers.click_element(self.driver, locators.first_active_date_xpath)

    def click_select_activity_button(self):
        """
        Clicks the select activity button to choose the activity option.
        
        Returns:
            None
        """
        driver_helpers.click_element(self.driver, locators.button_select_activity_xpath, timeout=10)

    def get_activity_price(self):
        """
        Retrieves the activity price from the footer section.
        
        Returns:
            str: The activity price as displayed on the page.
        """
        price = driver_helpers.get_text_from_element(self.driver, locators.activity_footer_price_xpath)
        log.info(f"Activity price: {price}")
        return price

    def click_add_activity_to_cart_button(self):
        """
        Clicks the add to cart button to add the selected activity to cart.
        
        Returns:
            None
        """
        driver_helpers.click_element(self.driver, locators.button_add_activity_to_cart_xpath, timeout=10)

    def click_view_cart_button(self):
        """
        Clicks the view cart button from the notification popup.
        
        Returns:
            None
        """
        driver_helpers.click_element(self.driver, locators.button_view_cart_notification_xpath, timeout=10)
