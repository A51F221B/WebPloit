import re
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import InvalidArgumentException, TimeoutException
import json
import urllib3

class Scanner: 
    def __init__(self, urls, template): 
        self.urls = urls 
        self.template = template


    def read_json_data(self):
        # Parse the JSON template and extract the necessary values
        try:
            # Try to parse the JSON data in the template variable
            data = json.loads(self.template)

            # Extract the necessary values from the parsed JSON data
            headers = data["request"]["headers"]
            payloads = data["payloads"]
            method = data["request"]["method"]
            return headers, payloads,method

        except json.JSONDecodeError:
            # If the JSON data is invalid, return an empty list of headers and payloads
            return [], [] ,[]


    def matchers(self, body):
        # Check if any of the matchers match the response body
        for match in self.template["matches"]:
            # Check if the matcher type is "regex"
            if match["type"] == "regex":
                regex = match["regex"]
                # Compile the regular expression
                pattern = re.compile(regex)
                # Check if the regular expression matches the response body
                if pattern.search(body):
                    return True
            # Check if the matcher type is "exact"
            elif match["type"] == "exact":
                string = match["string"]
                # Check if the exact string matches the response body
                if string in body:
                    return True
        return False

   

    def requester(self, url):
        # Create an HTTP connection pool
        http = urllib3.PoolManager()

        # Iterate over the list of URLs
        for url in self.urls:
            # Iterate over the list of payloads
            for payload in self.payloads:
                # Insert the payload into the URL
                full_url = url.format(payloads=payload)

                # Send a GET request to the URL
                response = http.request('GET', full_url)

                # Check if the payload matches any of the matchers
                if self.matchers(response.data):
                    print("Vulnerability found")
                    break



    def scan(self):
        # Read the JSON data from the template
        method,headers, payloads = self.read_json_data()

        # Store the payloads in an instance variable for use in the requester method
        self.payloads = payloads
        # Iterate over the list of URLs
        print(payloads)
        for url in self.urls:
            # Continue scanning for vulnerabilities
            self.requester(url)


