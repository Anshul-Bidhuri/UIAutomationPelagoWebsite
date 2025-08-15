import requests
from Helpers import custom_logger
import time

log = custom_logger.get_logger()


def return_status_code_of_url(api_url: str, method_name: str, timeout: int = 30) -> int:
    """
    Makes an HTTP request to the specified URL and returns the status code.
    
    This function sends an HTTP request using the specified method and returns
    the HTTP status code. Includes error handling for common network issues.
    
    Args:
        api_url (str): The URL to make the request to. Should be a valid HTTP/HTTPS URL.
        method_name (str): HTTP method to use (e.g., 'get', 'post', 'put', 'delete').
        timeout (int, optional): Request timeout in seconds. Defaults to 30.
    
    Returns:
        int: HTTP status code (e.g., 200, 404, 500).
    
    Raises:
        requests.exceptions.RequestException: For network-related errors.
        requests.exceptions.Timeout: If the request times out.
        ValueError: If invalid parameters are provided.
    """
    if not api_url or not isinstance(api_url, str):
        raise ValueError(f"Invalid URL provided: {api_url}")
    
    if not method_name or not isinstance(method_name, str):
        raise ValueError(f"Invalid method name provided: {method_name}")
    
    method_name = method_name.lower()
    valid_methods = ['get', 'post', 'put', 'delete', 'patch', 'head', 'options']
    
    if method_name not in valid_methods:
        raise ValueError(f"Invalid HTTP method: {method_name}. Valid methods: {valid_methods}")
    
    start_time = time.time()
    
    try:
        log.info(f"Making {method_name.upper()} request to: {api_url}")
        
        response = requests.request(
            method=method_name, 
            url=api_url, 
            timeout=timeout,
            allow_redirects=True,
            headers={'User-Agent': 'UIAutomation-PelagoWebsite/1.0'}
        )
        
        status_code = response.status_code
        elapsed_time = round(time.time() - start_time, 2)
        
        log.info(f"✓ {method_name.upper()} {api_url} → {status_code} ({elapsed_time}s)")
        
        return status_code
        
    except requests.exceptions.Timeout:
        elapsed_time = round(time.time() - start_time, 2)
        log.error(f"✗ Timeout after {elapsed_time}s: {api_url}")
        raise
        
    except Exception as e:
        elapsed_time = round(time.time() - start_time, 2)
        log.error(f"✗ Unexpected error after {elapsed_time}s: {api_url} - {str(e)}")
        raise

