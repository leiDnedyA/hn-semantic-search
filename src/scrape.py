from bs4 import BeautifulSoup
import requests

def get_plaintext_from_url(url: str, timeout: int = 10) -> str:
    """
    Fetches the webpage at the given URL and returns its plaintext content from the <body>.
    
    Args:
        url (str): The URL to fetch.
        timeout (int): Timeout for the HTTP request in seconds.
        
    Returns:
        str: The plaintext content of the page body, or an empty string if failed.
    """
    try:
        response = requests.get(url, timeout=timeout)
        response.raise_for_status()
        soup = BeautifulSoup(response.content, "html.parser")

        # Extract body and clean it
        body = soup.body
        if body:
            return body.get_text(separator='\n', strip=True)
        return ""
    except (requests.RequestException, Exception) as e:
        print(f"Error fetching {url}: {e}")
        return ""
