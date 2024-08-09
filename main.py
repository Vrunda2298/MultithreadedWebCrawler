from mythread import MyThread
from globalParams import GlobalParams
from queue import Queue
import threading
import os
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


MAX_ALLOWED_THREADS = 5001


def create_url_queue(urls_file):
    queue = Queue()
    try:
        with open(urls_file) as file:
            for line in file:
                queue.put(line)

        file_size = os.stat(urls_file)
        print("Opened ", urls_file, " with size ", file_size.st_size)

    except IOError:
        print("File not found.")
        exit(1)

    return queue


def main():

    no_of_threads = input("Enter the number of threads, max " + str(MAX_ALLOWED_THREADS) + " allowed : ")
    file_name = input("Enter Filename : ")

    no_of_threads = int(no_of_threads) + 1

    if no_of_threads > MAX_ALLOWED_THREADS + 1:
        print("Exceeds max allowed threads")
        exit(1)

    url_queue = create_url_queue(file_name)
    print("Queue size:", url_queue.qsize())

    # Create 5 threads with unique ids
    threads_list = []

    params = GlobalParams()
    params.lock = threading.Lock()
    params.unique_hosts = set()
    params.unique_ips = set()
    params.url_queue = url_queue
    params.count[0] = url_queue.qsize()
    params.print_queue = Queue()
    params.active_threads = 0

    for i in range(no_of_threads):
        if i < no_of_threads - 1:
            thread_type = 'crawl'
        else:
            thread_type = 'print'
        my_thread = MyThread(i, "thread-" + str(i), thread_type, params)
        my_thread.start()
        threads_list.append(my_thread)

    # Wait for all threads to finish
    for t in threads_list:
        t.join()

    # print("total seconds", params.total_seconds)
    # print("Status codes", params.status_codes)

    print(" ---------------------------------------------------------------------------------------")
    extracted_urls = params.count[0] - params.url_queue.qsize()
    print("Extracted", extracted_urls , "URLs", "@", str(round(extracted_urls / params.total_seconds))+"/s")
    print("Looked up", params.success_dns, "DNS names", "@", str(round(params.success_dns / params.total_seconds))+"/s")
    print("Downloaded", params.robots_check, "robots", "@", str(round(params.robots_check / params.total_seconds))+"/s")
    print("Crawled", params.success_crawl, "pages", "@", str(round(params.success_crawl / params.total_seconds))+"/s", "(" + str(round((params.total_size/10**6), 2))+"MB)")
    print("Parsed", params.total_links, "links", "@", str(round(params.total_links / params.total_seconds)) + "/s")

    print("HTTP codes:", end=" ")
    for key in params.status_codes:
        print(key + " = " + str(params.status_codes[key]), end=" ")


if __name__ == '__main__':
    main()
