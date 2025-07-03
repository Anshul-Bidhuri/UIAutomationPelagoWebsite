import pytest, pytest_check as check
from Pages.cartpage import CartPage
from Pages.homepage import Homepage
from Pages.activitypage import ActivityPage
from Data import constant


@pytest.mark.AdditeminCart
@pytest.mark.CartPage
class TestAddItemInCart:

    @pytest.fixture(scope="class", autouse=True)
    def initiate_driver(self, request, initiate_browser_webdriver):
        request.cls.driver = initiate_browser_webdriver
        request.cls.driver.get(constant.CART_PAGE_URL.get(request.cls.server))
        request.cls.home_page_obj = Homepage(request.cls.driver)
        request.cls.cart_page_obj = CartPage(request.cls.driver)
        request.cls.activity_page_obj = ActivityPage(request.cls.driver)

    def test_empty_cart_message_visibility(self):
        """
        Checks that cart is empty and empty cart message is visible
        """
        check.equal(self.cart_page_obj.check_empty_cart_message_visibility(), True, msg="Empty cart message is not visible")


    def test_add_item_in_cart(self):
        """
        Test Adds an item in cart flow and compare the price present on cart page and activity page
        """
        self.cart_page_obj.click_explore_activities_button()
        self.home_page_obj.click_first_recommended_activity_for_you()
        self.home_page_obj.switch_to_newest_tab()
        self.activity_page_obj.click_first_active_date()
        self.activity_page_obj.click_select_activity_button()
        price_on_activity_page = self.activity_page_obj.get_activity_price()
        self.activity_page_obj.click_add_activity_to_cart_button()
        self.activity_page_obj.click_view_cart_button()
        price_on_cart_page = self.cart_page_obj.get_price_of_cart_item()
        check.equal(price_on_activity_page, price_on_cart_page, msg="Item price on cart page is not matching")
