from urllib.parse import urlparse
import validators


class MyParser:

    def parse_url(self, url):
        url = url.strip()
        parsed_url = urlparse(url)
        port = 80 if parsed_url.port is None else parsed_url.port
        path = '/' if len(parsed_url.path) <= 0 else parsed_url.path
        query = parsed_url.query if len(parsed_url.query) <= 0 else '?'+parsed_url.query
        # print("Debug", parsed_url.hostname, port, path, query)
        return parsed_url.hostname, path, query, port

    def validate_url(self, url):
        return validators.url(url)