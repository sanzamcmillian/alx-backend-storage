#!/usr/bin/env python3
""" Main file """

web = __import__('web').web

if __name__ == "__main__":
    test_url = "http://slowwly.robertomurray.co.uk/delay/5000/url/http://www.example.com"
    
    # Fetch the page content for the first time (this will take time due to the delay)
    print("Fetching the page for the first time...")
    print(get_page(test_url))

    # Fetch the page content again (this should be served from the cache)
    print("Fetching the page again (should be cached)...")
    print(get_page(test_url))