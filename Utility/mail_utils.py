import os
import re
from typing import Dict, Any
from datetime import datetime
from bs4 import BeautifulSoup
from Utility.AWS.s3_methods import upload_report_to_s3
from Utility.GCP.gmail_methods import send_mail


def generate_email_html(report_data: Dict[str, Any]) -> str:
    """
    Generates HTML email content for test report notifications.
    
    Args:
        report_data (Dict[str, Any]): Dictionary containing test report data with keys:
            - total_tests: Total number of tests executed
            - passed_tests: Number of passed tests
            - failed_tests: Number of failed tests
            - skipped_tests: Number of skipped tests
            - browser_name: Browser used for testing
            - test_environment: Environment (PROD/QA)
            - execution_time: Test execution duration
            - report_s3_url: S3 URL where detailed report is stored
            - build_id: Build/execution identifier
    
    Returns:
        str: Complete HTML email content ready to send.
    """
    # Read the HTML template
    template_path = os.path.join(os.path.dirname(__file__), 'email_template.html')
    with open(template_path, 'r', encoding='utf-8') as file:
        html_template = file.read()
    
    # Calculate success rate
    total = report_data.get('total_tests', 0)
    passed = report_data.get('passed_tests', 0)
    success_rate = round((passed / total * 100), 1) if total > 0 else 0
    
    # Determine test status
    failed = report_data.get('failed_tests', 0)
    if failed == 0:
        test_status = "passed"
        test_status_text = "All Tests Passed ✅"
    elif passed == 0:
        test_status = "failed"
        test_status_text = "All Tests Failed ❌"
    else:
        test_status = "mixed"
        test_status_text = "Mixed Results ⚠️"
    
    # Replace placeholders with actual data
    replacements = {
        '{TEST_STATUS}': test_status,
        '{TEST_STATUS_TEXT}': test_status_text,
        '{TOTAL_TESTS}': str(report_data.get('total_tests', 0)),
        '{PASSED_TESTS}': str(report_data.get('passed_tests', 0)),
        '{FAILED_TESTS}': str(report_data.get('failed_tests', 0)),
        '{SKIPPED_TESTS}': str(report_data.get('skipped_tests', 0)),
        '{BROWSER_NAME}': report_data.get('browser_name', 'Chrome').title(),
        '{TEST_ENVIRONMENT}': report_data.get('test_environment', 'PROD'),
        '{EXECUTION_TIME}': report_data.get('execution_time', 'N/A'),
        '{SUCCESS_RATE}': str(success_rate),
        '{REPORT_S3_URL}': report_data.get('report_s3_url', '#'),
        '{REPORT_TIMESTAMP}': report_data.get('report_timestamp', 'N/A')
    }
    
    # Apply all replacements
    for placeholder, value in replacements.items():
        html_template = html_template.replace(placeholder, value)
    
    return html_template


def parse_pytest_html_report() -> Dict[str, Any]:
    """
    Parses pytest HTML report to extract test execution details and configuration.

    Returns:
        Dict[str, Any]: Dictionary containing parsed test data with keys:
            - total_tests: Total number of tests
            - passed_tests: Number of passed tests
            - failed_tests: Number of failed tests
            - skipped_tests: Number of skipped tests
            - xfailed_tests: Number of expected failures
            - xpassed_tests: Number of unexpected passes
            - error_tests: Number of tests with errors
            - rerun_tests: Number of reruns
            - execution_time: Test execution duration
            - browser_name: Browser used for testing
            - test_environment: Environment (PROD/QA)
            - report_timestamp: When the report was generated
    """
    report_file_path = os.path.join(os.path.abspath(__file__ + "/../../"), 'new_report.html')
    try:
        with open(report_file_path, 'r', encoding='utf-8') as file:
            html_content = file.read()
        
        soup = BeautifulSoup(html_content, 'html.parser')
        
        # Initialize result dictionary
        result = {
            'total_tests': 0,
            'passed_tests': 0,
            'failed_tests': 0,
            'skipped_tests': 0,
            'xfailed_tests': 0,
            'xpassed_tests': 0,
            'error_tests': 0,
            'rerun_tests': 0,
            'execution_time': 'N/A',
            'browser_name': 'N/A',
            'test_environment': 'N/A',
            'report_timestamp': 'N/A'
        }
        
        # Parse filters section for test counts
        filters_div = soup.find('div', class_='filters')
        if filters_div:
            # Extract failed count
            failed_span = filters_div.find('span', class_='failed')
            if failed_span:
                failed_text = failed_span.get_text()
                failed_match = re.search(r'(\d+)\s+Failed', failed_text)
                if failed_match:
                    result['failed_tests'] = int(failed_match.group(1))
            
            # Extract passed count
            passed_span = filters_div.find('span', class_='passed')
            if passed_span:
                passed_text = passed_span.get_text()
                passed_match = re.search(r'(\d+)\s+Passed', passed_text)
                if passed_match:
                    result['passed_tests'] = int(passed_match.group(1))
            
            # Extract skipped count
            skipped_span = filters_div.find('span', class_='skipped')
            if skipped_span:
                skipped_text = skipped_span.get_text()
                skipped_match = re.search(r'(\d+)\s+Skipped', skipped_text)
                if skipped_match:
                    result['skipped_tests'] = int(skipped_match.group(1))
            
            # Extract xfailed count
            xfailed_span = filters_div.find('span', class_='xfailed')
            if xfailed_span:
                xfailed_text = xfailed_span.get_text()
                xfailed_match = re.search(r'(\d+)\s+Expected failures', xfailed_text)
                if xfailed_match:
                    result['xfailed_tests'] = int(xfailed_match.group(1))
            
            # Extract xpassed count
            xpassed_span = filters_div.find('span', class_='xpassed')
            if xpassed_span:
                xpassed_text = xpassed_span.get_text()
                xpassed_match = re.search(r'(\d+)\s+Unexpected passes', xpassed_text)
                if xpassed_match:
                    result['xpassed_tests'] = int(xpassed_match.group(1))
            
            # Extract error count
            error_span = filters_div.find('span', class_='error')
            if error_span:
                error_text = error_span.get_text()
                error_match = re.search(r'(\d+)\s+Errors', error_text)
                if error_match:
                    result['error_tests'] = int(error_match.group(1))
            
            # Extract rerun count
            rerun_span = filters_div.find('span', class_='rerun')
            if rerun_span:
                rerun_text = rerun_span.get_text()
                rerun_match = re.search(r'(\d+)\s+Reruns', rerun_text)
                if rerun_match:
                    result['rerun_tests'] = int(rerun_match.group(1))
        
        # Parse execution time from run-count paragraph
        run_count_p = soup.find('p', class_='run-count')
        if run_count_p:
            run_count_text = run_count_p.get_text()
            # Extract total tests count
            total_match = re.search(r'(\d+)\s+tests?', run_count_text)
            if total_match:
                result['total_tests'] = int(total_match.group(1))
            
            # Extract execution time
            time_match = re.search(r'took\s+(\d{2}:\d{2}:\d{2})', run_count_text)
            if time_match:
                result['execution_time'] = time_match.group(1)
        
        # Extract browser and environment configuration
        # Method 1: Look for the config info we added in conftest.py
        config_info = soup.find('p', id='test-config-info')
        if config_info:
            config_text = config_info.get_text()
            # Parse: "Browser: Chrome | Environment: PROD | Headless: False"
            
            # Extract browser
            browser_match = re.search(r'Browser:\s*(\w+)', config_text, re.IGNORECASE)
            if browser_match:
                result['browser_name'] = browser_match.group(1).lower()
            
            # Extract environment
            env_match = re.search(r'Environment:\s*(\w+)', config_text, re.IGNORECASE)
            if env_match:
                result['test_environment'] = env_match.group(1).upper()
        
        # Method 2: Fallback - search in all text content
        else:
            text_content = soup.get_text().lower()
            
            # Extract browser from text content
            if 'firefox' in text_content:
                result['browser_name'] = 'FIREFOX'
            elif 'safari' in text_content:
                result['browser_name'] = 'SAFARI'
            elif 'chrome' in text_content:
                result['browser_name'] = 'CHROME'
            
            # Extract environment from text content
            if 'qa' in text_content and 'environment' in text_content:
                result['test_environment'] = 'QA'
            elif 'prod' in text_content and 'environment' in text_content:
                result['test_environment'] = 'PROD'
        
        # Extract report generation timestamp
        # Look for pattern: "Report generated on 15-Aug-2025 at 16:45:09 by pytest-html"
        timestamp_match = re.search(r'Report generated on (\d{1,2}-\w{3}-\d{4} at \d{2}:\d{2}:\d{2})', html_content)
        if timestamp_match:
            result['report_timestamp'] = timestamp_match.group(1)
        
        return result
        
    except Exception as e:
        print(f"Error parsing pytest HTML report: {str(e)}")
        return {
            'total_tests': 0,
            'passed_tests': 0,
            'failed_tests': 0,
            'skipped_tests': 0,
            'xfailed_tests': 0,
            'xpassed_tests': 0,
            'error_tests': 0,
            'rerun_tests': 0,
            'execution_time': 'N/A',
            'browser_name': 'NA',
            'test_environment': 'NA',
            'report_timestamp': 'N/A'
        }


def generate_email_body_from_report(report_s3_url: str = '#') -> str:
    """
    Generates email HTML by parsing pytest report and extracting all configuration.
    
    Args:
        report_s3_url (str): S3 URL where the report is uploaded.
    
    Returns:
        str: Complete HTML email content.
    """
    # Parse the pytest report for test results and configuration
    parsed_data = parse_pytest_html_report()
    
    # Add the S3 URL
    parsed_data['report_s3_url'] = report_s3_url
    
    # Generate and return email HTML
    return generate_email_html(parsed_data)


def upload_report_and_send_mail():
    s3_url = upload_report_to_s3()
    if s3_url:
        current_time = datetime.now().strftime("%d/%m/%Y %I:%M %p")
        subject = f"Pelago UI Automation Report | {current_time}"
        email_body = generate_email_body_from_report(s3_url)
        send_mail(subject, email_body)