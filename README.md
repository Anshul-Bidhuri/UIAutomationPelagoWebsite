# UI Automation Framework for Pelago Website

A comprehensive Selenium-based UI automation testing framework for the Pelago travel website, built with Python and pytest. This framework follows the Page Object Model (POM) design pattern and includes robust test reporting capabilities.

## 🚀 Features

- **Multi-browser Support**: Chrome, Firefox, and Safari
- **Cross-environment Testing**: Support for PROD and QA environments
- **Page Object Model**: Clean separation of test logic and page interactions
- **Headless Mode**: Option to run tests in headless mode for CI/CD
- **Detailed Reporting**: HTML reports with custom formatting and logging
- **Robust Element Handling**: Advanced wait strategies and popup handling
- **API Validation**: Status code validation for links and images
- **Custom Logging**: Comprehensive logging with timestamps and file output

## 📁 Project Structure

```
UIAutomationPelagoWebsite/
├── conftest.py                 # Pytest configuration and fixtures
├── pytest.ini                 # Pytest settings and markers
├── locators.py                 # Web element locators (XPath, CSS)
├── requirements.txt           # Python dependencies
├── new_report.html            # Generated test report
├── README.md                  # Project documentation
├── Data/
│   └── constant.py            # Environment URLs and constants
├── Helpers/
│   ├── assertion_methods.py   # Custom assertion utilities
│   ├── custom_logger.py       # Logging configuration
│   └── driver_helpers.py      # WebDriver utilities and helper functions
├── Pages/
│   ├── basepage.py           # Base page class with common methods
│   ├── homepage.py           # Homepage page object
│   ├── cartpage.py           # Cart page page object
│   └── activitypage.py       # Activity page page object
├── tests/
│   ├── test_homepage.py      # Homepage test scenarios
│   └── test_cart_page.py     # Cart functionality tests
└── Utility/
    └── api_services.py       # API utility functions
```

## 🛠️ Setup and Installation

### Prerequisites

- Python 3.7+
- pip (Python package installer)
- Chrome/Firefox/Safari browser installed

### Installation

1. **Clone the repository**:
   ```bash
   git clone <repository-url>
   cd UIAutomationPelagoWebsite
   ```

2. **Create a virtual environment** (recommended):
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

## 🎯 Usage

### Running Tests

#### Basic Test Execution

```bash
# Run all tests with default settings (Chrome, PROD environment)
pytest

# Run specific test file
pytest tests/test_homepage.py

# Run specific test class
pytest tests/test_homepage.py::TestFamousDestinationSection

# Run specific test method
pytest tests/test_homepage.py::TestFamousDestinationSection::test_famous_destination_links_status_code
```

#### Browser Selection

```bash
# Run tests in Firefox
pytest -B firefox

# Run tests in Safari
pytest -B safari

# Run tests in Chrome (default)
pytest -B chrome
```

#### Parallel Test Execution

```bash
# Run tests in parallel with 3 workers, distributing by test scope
pytest -n 3 --dist=loadscope

# Combine parallel execution with other options
pytest -n 3 --dist=loadscope -B firefox -S PROD
```

#### Environment Selection

```bash
# Run tests against QA environment
pytest -S QA

# Run tests against PROD environment (default)
pytest -S PROD
```

#### Headless Mode

```bash
# Run tests in headless mode
pytest -H True
```

#### Combined Options

```bash
# Run tests in Firefox, QA environment, headless mode
pytest -B firefox -S QA -H True

# Run specific tests with custom browser and environment
pytest tests/test_cart_page.py -B chrome -S PROD

# Run tests in parallel with custom options
pytest -n 3 --dist=loadscope -B firefox -S QA -H True
```

### Test Markers

The framework uses pytest markers to categorize tests:

```bash
# Run tests marked as FamousDestinationSection
pytest -m FamousDestinationSection

# Run tests marked as HomePage
pytest -m HomePage

# Run tests marked as CartPage
pytest -m CartPage
```

### HTML Reporting

Tests automatically generate HTML reports with detailed results:

```bash
# Generate HTML report (default behavior)
pytest --html=new_report.html --self-contained-html
```

## 🧪 Test Scenarios

### Homepage Tests (`test_homepage.py`)

1. **Famous Destination Links Validation**
   - Verifies all destination tile links return HTTP 200 status code
   - Tests link accessibility and validity

2. **Famous Destination Images Validation**
   - Checks all destination images load successfully
   - Validates image URL accessibility

3. **Ongoing Deals Section**
   - Verifies the presence of exactly 6 ongoing deals tiles
   - Tests section visibility and content

### Cart Page Tests (`test_cart_page.py`)

1. **Empty Cart Validation**
   - Confirms empty cart message visibility
   - Tests initial cart state

2. **Add Item to Cart Flow**
   - Complete end-to-end test for adding items to cart
   - Price validation between activity page and cart page
   - Multi-page navigation testing

## 🏗️ Framework Architecture

### Page Object Model

The framework implements the Page Object Model pattern:

- **BasePage**: Contains common page operations (navigation, tab switching)
- **HomePage**: Homepage-specific interactions and element handling
- **CartPage**: Cart functionality and validations
- **ActivityPage**: Activity selection and booking operations

### Helper Modules

- **driver_helpers.py**: WebDriver utilities, wait strategies, element interactions
- **custom_logger.py**: Centralized logging with file output and formatting
- **assertion_methods.py**: Custom assertion methods for API validation

### Configuration

- **conftest.py**: Pytest fixtures, command-line options, and HTML report customization
- **pytest.ini**: Test markers, logging configuration
- **locators.py**: Centralized element locators using XPath

## 📊 Logging and Reporting

### Logging Features

- Automatic log file generation with timestamps
- Console and file logging with different levels
- Detailed element interaction logging
- Error tracking and debugging information

### HTML Reports

- Custom HTML reports with test descriptions
- Pass/fail status with detailed error messages
- Execution time and environment information
- Screenshots on failure (can be extended)


## 📄 License

This project is created by **Anshul Bidhuri** for UI automation testing of the Pelago website.

---

**Framework Version**: 1.0  
**Last Updated**: Aug 2025  
**Author**: Anshul Bidhuri