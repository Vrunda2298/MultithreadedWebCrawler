class GlobalParams:
    def __init__(self):
        self.url_queue = None
        self.lock = None
        self.unique_hosts = None
        self.unique_ips = None
        self.print_queue = None
        self.count = [1]
        self.active_threads = 0
        self.total_url_count = 0
        self.success_dns = 0
        self.robots_check = 0
        self.success_crawl = 0
        self.total_links = 0
        self.total_size = 0
        self.total_seconds = 0
        self.status_codes = dict()
        self.status_codes['2xx'] = 0
        self.status_codes['3xx'] = 0
        self.status_codes['4xx'] = 0
        self.status_codes['5xx'] = 0
        self.status_codes['other'] = 0
