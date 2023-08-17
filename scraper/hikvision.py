from typing import Optional, Dict, List
from bs4 import BeautifulSoup
import requests
from urllib.parse import urlparse
import concurrent.futures
from .firmware_webpage import FirmwareWebPage

NUM_THREADS = 5
MOZILLA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36"
HEADERS = {
    "User-Agent": MOZILLA,
    "accept": "*/*",
}

def get_all_firmwares(url: str) -> Optional[Dict]:
    firmwares = {}
    urls_to_scrape: List[str] = []
    pages_content = []

    html = scrape_page(url)

    if html is None:
        return None
    
    parse_result = urlparse(url)
    domain_url = parse_result.scheme + "://" + parse_result.hostname
    links = find_links_with_firmwares(html, parse_result.path)
    urls_to_scrape = list(map(lambda x: domain_url + x, links))

    with concurrent.futures.ThreadPoolExecutor(max_workers=NUM_THREADS) as executor:
        pages_content = list(executor.map(scrape_page, urls_to_scrape[:1]))

    for current_page in pages_content:
        firmware_page = FirmwareWebPage(html=current_page)
        print(firmware_page.get_firmware_list())        

    return firmwares


def find_links_with_firmwares(html: BeautifulSoup, path_pattern: str) -> List:
    links = []
    side_menu = html.find('div',"menu-name-main-menu")
    
    for element in side_menu.select(f'a[href^=\"{path_pattern}\"]'):
        links.append(element['href'])

    return links


def scrape_page(url: str) -> Optional[BeautifulSoup]:

    try:
        request_response = requests.get(url, headers=HEADERS)
        
        if request_response.status_code == 200:
            return BeautifulSoup(request_response.content, 'html5lib')
        
    except Exception as e:
        print("An error occurred:", str(e))
        return None
