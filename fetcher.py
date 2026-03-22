
# fetcher.py
# Download the border wait page

import requests

URL = "https://granica.gov.pl/index_wait.php?p=u&v=en"

HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (iPhone; CPU iPhone OS 17_0 like Mac OS X) "
        "AppleWebKit/605.1.15 (KHTML, like Gecko) "
        "Version/17.0 Mobile/15E148 Safari/604.1"
    )
}


def fetch_data():
    response = requests.get(URL, headers=HEADERS, timeout=10)
    response.raise_for_status()
    return response.text
    
    
