from typing import Optional, List, Any
from bs4 import BeautifulSoup
import requests

MOZILLA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36"
HEADERS = {
    "User-Agent": MOZILLA,
    "accept": "*/*",
}

def get_html_content(url: str) -> Optional[BeautifulSoup]:
    try:
        request_response = requests.get(url, headers=HEADERS)
        return BeautifulSoup(request_response.content, 'html5lib')
    except Exception as e:
        print("An error occurred:", str(e))
        return None
