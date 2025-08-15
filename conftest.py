import pytest
from py.xml import html

from Helpers import driver_helpers


@pytest.fixture(scope="class")
def initiate_browser_webdriver(request):
    """
    Pytest fixture that initializes and provides a WebDriver instance for test classes.
    
    Args:
        request: Pytest request object containing command line options and test context.
    
    Returns:
        WebDriver: Configured WebDriver instance based on command line options.
    """
    browser_option = request.config.getoption("Browser")
    server_option = request.config.getoption("Server")
    headless_option = request.config.getoption("Headless")
    request.cls.server = server_option
    driver_options = {
        "chrome": driver_helpers.initialize_chrome_driver,
        "firefox": driver_helpers.initialize_firefox_driver,
        "safari": driver_helpers.initialize_safari_driver}
    driver = driver_options[browser_option](headless_option)
    yield driver
    driver.quit()


def pytest_addoption(parser):
    """
    Adds custom command line options for pytest execution.
    
    Args:
        parser: Pytest argument parser for adding custom command line options.
    
    Returns:
        None
    """
    group = parser.getgroup("general")
    group._addoption(
        "-B",
        dest="Browser",
        default="chrome",
        help="Browser to use. Options are: chrome, firefox and safari. Example: -B firefox",
    )
    group._addoption(
        "-S",
        dest="Server",
        default="PROD",
        help="Server to use. Options are: QA, PROD. Example: -S PROD",
    )
    group._addoption(
        "-H",
        dest="Headless",
        default=False,
        help="Run in headless mode. Example: -H True",
    )


def pytest_html_results_summary(prefix, session):
    """
    Customizes the HTML report summary section with framework information.
    
    Args:
        prefix: List of HTML elements to be added to the report summary.
        session: Pytest session object containing configuration.
    
    Returns:
        None
    """
    # Get browser and environment from pytest config
    browser = session.config.getoption("Browser", default="chrome")
    server = session.config.getoption("Server", default="PROD")
    headless = session.config.getoption("Headless", default=False)
    
    prefix.extend([
        html.p("This UI Automation regression framework is created by ANSHUL BIDHURI"),
        html.p(f"Browser: {browser.title()} | Environment: {server} | Headless: {headless}", 
               id="test-config-info", style="color: #666; font-size: 14px; margin: 5px 0;")
    ])


def pytest_html_results_table_header(cells):
    """
    Customizes the HTML report table header by adding a Description column.
    
    Args:
        cells: List of HTML table header cells to be modified.
    
    Returns:
        None
    """
    cells.insert(1, html.th("Description"))
    cells.pop(2)
    cells.pop()  # to remove last column name


def pytest_html_results_table_row(report, cells):
    """
    Customizes HTML report table rows by adding test description data.
    
    Args:
        report: Pytest test report object containing test execution details.
        cells: List of HTML table cells to be modified.
    
    Returns:
        None
    """
    cells.insert(1, html.td(report.description))
    cells.pop(2)
    cells.pop()  # to remove last row values


@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """
    Pytest hook that captures test function docstrings for HTML report descriptions.
    
    Args:
        item: Pytest test item containing test function information.
        call: Pytest call object containing test execution phase information.
    
    Returns:
        None
    """
    outcome = yield
    report = outcome.get_result()
    report.description = str(item.function.__doc__)
