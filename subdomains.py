from queue import Queue
import requests
import re
from bs4 import BeautifulSoup
from config import API_key
from threading import Thread
import shodan
import json
import urllib
import pandas as pd
from urllib.parse import urlparse
from requests_html import HTML
from requests_html import HTMLSession


class GoogleEnum:
    """
    This class will make using of simple google searches via google dorks to enlist subdomains
    """
    subdomains=[] 

    def __init__(self,url) -> None:
        self.url=url
        self.GetDomain()

    def ReturnSourceCode(self,query):
        """Return the source code for the provided URL. 

        Args: 
            url (string): URL of the page to scrape.

        Returns:
            response (object): HTTP response object from requests_html. 
        """

        try:
            session = HTMLSession()
            response = session.get(query)
            return response ## returns 200 if OK

        except requests.exceptions.RequestException as e:
            print(e)


    def scrape_google(self,query):

        query = urllib.parse.quote_plus(query)
        link=f'https://www.google.com/search?client=firefox-b-d&q=site:{query}'
        response = GoogleEnum.ReturnSourceCode(self,link)

        links = list(response.html.absolute_links) ## getting all the links from search result
        google_domains = ('https://www.google.', 
                        'https://google.', 
                        'https://webcache.googleusercontent.', 
                        'http://webcache.googleusercontent.', 
                        'https://policies.google.',
                        'https://support.google.',
                        'https://maps.google.')

        for url in links[:]:
            if url.startswith(google_domains): # removing links with google_domains in it
                links.remove(url)
                #self.subdomains=links # adding these links to our one universal list for keeping domains
        return links
    

    def GetUniqueDomains(self,links):
        for link in links:
            parsed=urlparse(link).netloc
            self.subdomains.append(parsed)
        result = [i for n, i in enumerate(self.subdomains) if i not in self.subdomains[:n]] 
        return result



    def GetDomain(self):
         print(self.GetUniqueDomains(self.scrape_google(self.url)))
    

class Shodan:
    """
    This class is using Shodan Search engine via a shodan API to enlist subdomains
    """
    api=shodan.Shodan(API_key)

    def SearchDomains(self,url):
        r=requests.get(f'https://api.shodan.io/dns/domain/{url}?key={API_key}')
        data=json.loads(r.text) ## reading json data from return in r.text
        ## load() and loads() for turning JSON encoded data into Python objects.
        print(data)
        
        

class Dictionary:
    """
    This takes a simple bruteforce approach towards subdomains finding by simply providing a input file
    """
    q = Queue()
    numThreads = 20

    def __runner__(self, domain):
        subdomain = self.q.get()
        print(f"Current domain: {subdomain}")
        url1 = f"http://{subdomain}.{domain}"
        url2 = f"https://{subdomain}.{domain}"
        try:
            print("Fetching:{}".format(url1))
            requests.get(url1)
            print(f"Discovered URL: {url1}")
            requests.get(url2)
            print(f"Discovered URL: {url2}")
        except requests.ConnectionError:
            pass
        self.q.task_done()


    def FindDomain(self,domain):
        file = open('wordlist.txt','r')
        content = file.read()
        subdomains = content.splitlines()


        # for th in range(self.numThreads):
        #     th = Thread(target=self.__runner__, args=(domain,), daemon=True)
        #     th.start()
        
        # for subdomain in subdomains:
        #     self.q.put(subdomain)
		
        # self.q.join()


        # for subdomain in subdomains:
        #     url1 = f"http://{subdomain}.{domain}"
        #     url2 = f"https://{subdomain}.{domain}"
        #     try:
        #         requests.get(url1)
        #         print(f"Discovered URL: {url1}")
        #         requests.get(url2)
        #         print(f"Discovered URL: {url2}")
        #     except requests.ConnectionError:
        #         pass








