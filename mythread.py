
import threading
from datetime import datetime
from myparser import MyParser
from myrequest import MyRequest
from serverconnect import ServerConnect
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


class MyThread(threading.Thread):

    def __init__(self, thread_id, thread_name, thread_type, params):
        threading.Thread.__init__(self)
        self.thread_id = thread_id
        self.thread_name = thread_name
        self.params = params
        self.thread_type = thread_type

    def run(self):
        if self.thread_type == 'crawl':
            self.crawl()
        else:
            self.print_details()

    def print_details(self):
        now = datetime.now()
        start = 0
        try:
            while True:
                later = datetime.now()
                difference = int((later - now).total_seconds())
                
                if difference < 2:
                    continue
                    
                self.params.lock.acquire()
                if not self.params.url_queue.empty():
                    self.params.lock.release()
                    single_stmt = self.create_print_statement()

                    seconds = start + difference
                    self.params.total_seconds = seconds

                    page_per_second = round(self.params.success_crawl / seconds, 1)
                    mb_per_second = round(((self.params.total_size / 10**6) / seconds), 1)
                    
                    print("[ " + str(start+difference) + "]", single_stmt)
                    print("     *** crawling", page_per_second, "pps @", mb_per_second, "Mbps")
                else:
                    self.params.lock.release()
                    break
                    
                start += difference
                now = datetime.now()
        except Exception as e:
            pass

    def create_print_statement(self):
        # Lock acquired
        self.params.lock.acquire()
        print_stats = ''
        print_stats += ' ' + str(self.params.active_threads)
        qsize = self.params.url_queue.qsize()
        print_stats += '  Q ' + str(qsize)
        print_stats += '  E ' + str(self.params.count[0] - qsize)
        print_stats += '  H ' + str(len(self.params.unique_hosts)) if self.params.unique_hosts is not None else 0
        print_stats += '  D ' + str(self.params.success_dns)
        print_stats += '  I ' + str(len(self.params.unique_ips)) if self.params.unique_ips is not None else 0
        print_stats += '  R ' + str(self.params.robots_check)
        print_stats += '  C ' + str(self.params.success_crawl)
        print_stats += '  L ' + str(self.params.total_links)
        self.params.lock.release()
        # Lock released
        
        return print_stats

    def crawl(self):
        self.params.lock.acquire()
        self.params.active_threads += 1
        self.params.lock.release()
        while True:
            # Lock acquired
            self.params.lock.acquire()
            if self.params.url_queue.qsize() < 1 :
                self.params.lock.release()
                break
            single_url = self.params.url_queue.get() # Pops the first element and Returns the value
            
            my_parser = MyParser()

            # Validate Input URL
            validated = my_parser.validate_url(single_url)
            if not validated:
                self.params.lock.release()
                continue

            # Parse URL
            host, path, query, port = my_parser.parse_url(single_url)
            
            prev_len_host = len(self.params.unique_hosts)
            self.params.unique_hosts.add(single_url)
            curr_len_host = len(self.params.unique_hosts)
            self.params.lock.release()
            # Lock released

            if curr_len_host == prev_len_host:
                continue

            my_server_connect = ServerConnect()

            ip = my_server_connect.get_ip(host)

            if ip is None:
                continue

            # Lock acquired
            self.params.lock.acquire()
            self.params.success_dns += 1
            prev_len_ip = len(self.params.unique_ips)
            self.params.unique_ips.add(ip)
            curr_len_ip = len(self.params.unique_ips)    
            self.params.lock.release()
            # Lock released

            if prev_len_ip == curr_len_ip:
                continue
            

            my_req = MyRequest()
            req = my_req.head_request(single_url, host)
            head_response = my_server_connect.get_html(req, query)
            if head_response is None:
                continue

            if hasattr(head_response, 'status_code'):
                if head_response.status_code != 404:
                    continue
            else:
                continue

            self.params.lock.acquire()
            self.params.robots_check += 1
            self.params.lock.release()

            response = my_server_connect.get_html(my_req.get_request(single_url), query)

            if response is None:
                continue

            if hasattr(response, 'status_code'):
                self.params.lock.acquire()
                dict_key = str(response.status_code)[0]+"xx"

                if dict_key in self.params.status_codes:
                    self.params.status_codes[dict_key] += 1
                else:
                    self.params.status_codes['other'] += 1

                self.params.lock.release()

                if response.status_code != 200:
                    continue
            else:
                continue
            
            self.params.lock.acquire()
            self.params.success_crawl += 1
            total_links = my_server_connect.parse_data(response.content)
            if total_links is not None:
                self.params.total_links += total_links
                self.params.total_size += len(response.content)

            self.params.lock.release()
