import socket
import requests
from bs4 import BeautifulSoup
    
TIMEOUT = 10
SIZE_LIMIT = 2000000    # 2MB


class ServerConnect:

    def __init__(self):
        self.host = ''

    def get_ip(self, hostname):
        try:
            ip = socket.gethostbyname(hostname)
        except socket.error as e:
            ip = None
        return ip

    def get_html(self, url, query):
        try:
            if query.strip() == "?download=1":
                return None
            response = requests.get(url['req'], headers=url['header'], verify=False, timeout=TIMEOUT)
            if len(response.content) > SIZE_LIMIT:
                return None
            return response
        except Exception as e:
            # print ("error on request", e)
            return e

    def extract_links(self, soup):
        try:
            arr = soup.find_all('a')
            return len(arr)
        except Exception as e:
            # print(e)
            return 0

    def parse_data(self, html):
        try:
            soup = BeautifulSoup(html, 'html.parser')
            links = self.extract_links(soup)
            return links
        except Exception as e:
            return None
