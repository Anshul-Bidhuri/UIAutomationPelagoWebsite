import sys, os
import time

main_project_path = os.path.abspath(__file__+"../../../")
sys.path.append(main_project_path)

from Pages.basepage import BasePage
from Helpers import driver_helpers, custom_logger
import locators

log = custom_logger.get_logger()

class Homepage(BasePage):
    """
    Page object class for handling interactions with the Homepage.
    """

    def get_famous_destinations_elements(self):
        """
        Retrieves all famous destination elements from the homepage.
        
        Returns:
            list: List of WebElements representing famous destinations.
        """
        driver_helpers.wait_till_element_is_present(self.driver, locators.famous_destinations_title_xpath)
        famous_destinations = driver_helpers.get_all_elements(self.driver, locators.famous_destinations_title_xpath)
        log.info(f"famous destinations found: {len(famous_destinations)}")
        return famous_destinations

    def get_famous_destination_tile_links(self):
        """
        Extracts all links from famous destination tiles.
        
        Returns:
            list: List of URLs from famous destination tiles.
        """
        total_links = []
        famous_destinations = self.get_famous_destinations_elements()
        for destination in famous_destinations:
            driver_helpers.click_element(self.driver, element=destination, timeout=10)
            links = driver_helpers.get_all_elements(self.driver, locators.famous_destinations_link_under_each_title_xpath)
            log.info(f"links found: {len(links)}")
            for link_element in links:
                link = driver_helpers.get_element_attribute_value(driver=self.driver, element=link_element, attribute_name="href")
                total_links.append(link)
        log.info(f"total links: {total_links}")
        return total_links

    def get_famous_destination_images(self):
        """
        Extracts all image URLs from famous destination tiles.
        
        Returns:
            list: List of image URLs from famous destination tiles.
        """
        images_links = []
        famous_destinations = self.get_famous_destinations_elements()
        for destination in famous_destinations:
            driver_helpers.click_element(self.driver, element=destination, timeout=10)
            img_elements = driver_helpers.get_all_elements(self.driver, locators.famous_destinations_image_under_each_title_xpath)
            log.info(f"Images found: {len(img_elements)}")
            for img_element in img_elements:
                image_url = driver_helpers.get_element_attribute_value(driver=self.driver, element=img_element, attribute_name="src")
                images_links.append(image_url)
        log.info(f"images links: {images_links}")
        return images_links

    def get_ongoing_deals_elements(self):
        """
        Retrieves all ongoing deals elements from the homepage.
        
        Returns:
            list: List of WebElements representing ongoing deals.
        """
        driver_helpers.wait_till_element_is_present(self.driver, locators.ongoing_deals_title_xpath)
        ongoing_deals = driver_helpers.get_all_elements(self.driver, locators.ongoing_deals_title_xpath)
        log.info(f"ongoing deals found: {len(ongoing_deals)}")
        return ongoing_deals

    def click_first_recommended_activity_for_you(self):
        """
        Clicks on the first recommended activity in the recommendation section.
        
        Returns:
            None
        """
        driver_helpers.click_element(self.driver, locators.recommended_for_you_titles_xpath, timeout=5)