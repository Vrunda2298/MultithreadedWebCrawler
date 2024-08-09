# MultithreadedWebCrawler

# Data Communication Assignment #


## CONFIGURATION REQUIREMENT
* python 3.5 and up
* Unzip the file assignment1_part3.zip to get the python executable files

## COMPILATION AND EXECUTION
Following Python Packages are reuired :
* BeautifulSoup
* Requests
* Queue
* Datetime
* os
* urllib3
* validators

## STEPS TO EXECUTE
* Run the main function or main file [main.py]
     - This will ask user to enter number of threads and file name.
     - Enter the number of threads, max 5000 allowed : ENTER NUMBER OF THREADS HERE
     - Enter Filename : 
* After entering number of threads and file name, press ENTER to start process.

So, the code will print the statistics every 2 seconds and will print final output which prints total number of unique IPs, valid DNS names, number of pages successfully crawled, robots check and number of links.


## CODE EXPLANATION
This project processes the input URL file and crawls all the URLs provided in file by using multithreading and shared parameters

main.py

* Accepts two inputs: number of threads and file name
* create_url_queue() method that adds the URLs from the file into a queue and finds the size of file
* Creates shared parameters
* Creates threads with shared parameters
* Prints statistics and runtime at the end


myhtread.py

* Implements thread by creating class that extends threading.Thread superclass 
* Keeps count of active threads
* Validates URL
* Finds whether the host and ip address are unique,
    - if unique then parse the URL
    - otherwise continue with next URL
* Sends head request to check robots.txt
* If head request status code = 404 and sends the get request 
* If status code = 200, then retrieves the total number of links in that URL  


myparser.py

* Parses the URL using library and returns host, port, path and query
* Validated the input URL using library validators


myrequest.py

* creates head request with the given host, port, request and query
* creates get request with the given host, port, request and query


serverconnect.py

* Imports requests and BeautifulSoup libraries
* Get IP address from hostname
* Extracts links from html data 
* Send head and get requests to server 
* Parse response using BeautifulSoup

globalParams.py

* This file declares the shared parameters like:
     - url_queue = None 
     - print_queue = None 
     - success_dns = 0 
     - robots_check = 0 
     - unique_ips = set()
     - unique_hosts = set()
     - total_seconds = 1 
     - status_codes = dict()
* 
