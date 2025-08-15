from Utility import api_services
from pytest_check import check
from Helpers import custom_logger
from typing import List, Optional

log = custom_logger.get_logger()


def check_status_code_of_urls(urls: List[str], expected_status_code: int = 200, timeout: Optional[int] = None) -> None:
    """
    Validates HTTP status codes for a list of URLs using soft assertions.
    
    This function performs HTTP GET requests to each URL in the provided list and validates
    that each URL returns the expected status code. Uses pytest-check for soft assertions,
    allowing all URLs to be tested even if some fail.
    
    Args:
        urls (List[str]): List of URLs to validate. Each URL should be a valid HTTP/HTTPS URL.
        expected_status_code (int, optional): Expected HTTP status code. Defaults to 200.
        timeout (Optional[int], optional): Request timeout in seconds. If None, uses default timeout.
    
    Returns:
        None
    """
    if not urls:
        log.warning("Empty URL list provided to check_status_code_of_urls")
        return
    
    log.info(f"Starting status code validation for {len(urls)} URLs (expected: {expected_status_code})")
    
    failed_urls = []
    
    for i, url in enumerate(urls, 1):            
        try:
            log.info(f"Checking URL {i}/{len(urls)}: {url}")
            status_code = api_services.return_status_code_of_url(
                api_url=url, 
                method_name="get",
                timeout=timeout if timeout is not None else 30
            )
            
            if status_code == expected_status_code:
                log.info(f"✓ URL validation passed: {url} returned {status_code}")
            else:
                log.error(f"✗ URL validation failed: {url} returned {status_code}, expected {expected_status_code}")
                failed_urls.append({"url": url, "actual": status_code, "expected": expected_status_code})
            
            check.equal(
                status_code, 
                expected_status_code, 
                msg=f"URL: {url} | Expected: {expected_status_code} | Actual: {status_code}"
            )
            
        except Exception as e:
            log.error(f"Exception occurred while checking {url}: {str(e)}")
            check.fail(f"Failed to check URL {url}: {str(e)}")