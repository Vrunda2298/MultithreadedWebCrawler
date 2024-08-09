class MyRequest:
    def __init__(self):
        self.request = dict()
        self.request['req'] = ''
        # by default, requests are done using HTTP 1.1, It supports both HTTP and HTTPS
        self.request['header'] = {"User-Agent": "Crawler/1.0", 'connection': 'close'}

    def get_request(self, url):
        """Build an HTTP GET request """
        self.request['req'] = url.strip()
        return self.request

    def head_request(self, url, host):
        """Build a HEAD request, to check if host has "robots.txt" file """
        url_arr = url.split("//")
        if len(url_arr) >= 2:
            self.request['req'] = url_arr[0] + "//" + host + "/robots.txt"
        return self.request