import os
import time
import pytest
import pytest_html
from py.xml import html

from Helpers import driver_helpers
from Utility.recorder import FFmpegRecorder


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


@pytest.fixture(scope="function", autouse=True)
def record_test(request):
    """Fixture to record each test using FFmpeg"""
    recording_folder = os.path.join(os.path.abspath(__file__ + "/../"), "Recordings")
    # Create reports/recordings folder if not exists
    os.makedirs(recording_folder, exist_ok=True)

    # Generate unique filename
    test_name = request.node.name
    timestamp = time.strftime("%d%m%Y-%H%M%S")
    video_file = f"{recording_folder}/{test_name}_{timestamp}.mp4"

    # Store video file path on the test item for later access
    request.node._video_file = video_file

    # Start recording
    recorder = FFmpegRecorder(filename=video_file)
    try:
        recorder.start()
        yield  # Run the actual test
    finally:
        # Stop recording after test (ensure it stops even if test fails)
        recorder.stop()
        
        # Verify video file was created
        if not os.path.exists(video_file):
            print(f"Warning: Video file was not created: {video_file}")
        else:
            file_size = os.path.getsize(video_file)
            print(f"Video recorded: {video_file} ({file_size} bytes)")


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
    Pytest hook that captures test function docstrings for HTML report descriptions
    and attaches video recordings to failed/passed tests.
    
    Args:
        item: Pytest test item containing test function information.
        call: Pytest call object containing test execution phase information.
    
    Returns:
        None
    """
    outcome = yield
    report = outcome.get_result()
    report.description = str(item.function.__doc__)
    
    # Attach video to HTML report for all test outcomes
    if report.when == "call":
        # Get the video file path from the fixture if it exists
        video_file = getattr(item, '_video_file', None)
        if video_file and os.path.exists(video_file):
            # Make video path relative to the report location
            # Try to get the actual report path from config, fallback to current directory
            html_path = getattr(item.config.option, 'htmlpath', 'new_report.html')
            if html_path:
                report_dir = os.path.dirname(os.path.abspath(html_path))
            else:
                report_dir = os.getcwd()
            relative_video_path = os.path.relpath(video_file, report_dir)
            
            # Create HTML video element
            video_html = f'''
            <div style="margin: 10px 0;">
                <h4>Test Recording:</h4>
                <video width="640" height="480" controls>
                    <source src="{relative_video_path}" type="video/mp4">
                    Your browser does not support the video tag.
                </video>
            </div>
            '''
            
            # Attach extra content to the report
            # Use 'extras' instead of 'extra' for newer pytest-html versions
            if hasattr(report, 'extras'):
                report.extras.append(pytest_html.extras.html(video_html))
            else:
                # Fallback for older versions
                extra = getattr(report, 'extra', [])
                extra.append(pytest_html.extras.html(video_html))
                report.extra = extra
