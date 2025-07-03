
class BasePage:
    def __init__(self, driver):
        self.driver = driver

    def reload_page(self):
        self.driver.refresh()

    def open_page(self, url):
        self.driver.get(url)

    def switch_to_newest_tab(self):
        self.driver.switch_to.window(self.driver.window_handles[-1])
