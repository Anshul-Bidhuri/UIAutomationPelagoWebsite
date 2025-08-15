
class BasePage:
    """
    Base page class providing common functionality for all page objects.
    """
    
    def __init__(self, driver):
        """
        Initializes the base page with a WebDriver instance.
        
        Args:
            driver (WebDriver): The Selenium WebDriver instance.
        """
        self.driver = driver

    def reload_page(self):
        """
        Reloads the current page.
        
        Returns:
            None
        """
        self.driver.refresh()

    def open_page(self, url):
        """
        Navigates to the specified URL.
        
        Args:
            url (str): The URL to navigate to.
            
        Returns:
            None
        """
        self.driver.get(url)

    def switch_to_newest_tab(self):
        """
        Switches focus to the newest opened browser tab.
        
        Returns:
            None
        """
        self.driver.switch_to.window(self.driver.window_handles[-1])
