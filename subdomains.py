from queue import Queue
from socket import timeout
from urllib import response
import requests
from config import API_key
from threading import Thread
import shodan
import json
import urllib
from urllib.parse import urlparse
from requests_html import HTML
from requests_html import HTMLSession
from concurrent.futures import ThreadPoolExecutor


class GoogleEnum:
    """
    This class will make using of simple google searches via google dorks to enlist subdomains.What
    actually is happening is that we are scarping links from different search engines and then removing
    the paths from those links and adding unique domains to a list.
    for example : https://au.edu.pk/results will be converted to au.edu.pk  
    """
    subdomains = []

    def __init__(self, url) -> None:
        self.url = url
        self.GetDomain()

    def ReturnSourceCode(self, query):
        """Return the source code for the provided URL. 

        Args: 
            url (string): URL of the page to scrape.

        Returns:
            response (object): HTTP response object from requests_html. 
        """

        try:
            session = HTMLSession()
            response = session.get(query)
            return response  # returns 200 if OK

        except requests.exceptions.RequestException as e:
            print(e)

    def scrape_google(self, query):

        query = urllib.parse.quote_plus(query)
        link = f'https://www.google.com/search?client=firefox-b-d&q=site:{query}'
        response = GoogleEnum.ReturnSourceCode(self, link)

        # getting all the links from search result
        links = list(response.html.absolute_links)
        google_domains = ('https://www.google.',
                          'https://google.',
                          'https://webcache.googleusercontent.',
                          'http://webcache.googleusercontent.',
                          'https://policies.google.',
                          'https://support.google.',
                          'https://maps.google.')

        for url in links[:]:
            # removing links with google_domains in it
            if url.startswith(google_domains):
                links.remove(url)
                # self.subdomains=links # adding these links to our one universal list for keeping domains
        return links

    # this function removes duplicate domains from the list and returns a list of unique domains
    def GetUniqueDomains(self, links):
        for link in links:
            parsed = urlparse(link).netloc  # removing the path from the link
            self.subdomains.append(parsed)  # adding the domain to the list
            exception = ['support.microsoft.com','go.microsoft.com', 'google.com']
        result = [i for n, i in enumerate(self.subdomains) if i not in self.subdomains[:n]]
        if self.url != 'microsoft.com' or self.url != 'google.com':
            try:
                for data in exception:
                    if data in result:
                        result.remove(data)
            except:
                pass
        self.subdomains = result.copy()
        return result

    def GetDomain(self):
        return self.GetUniqueDomains(self.scrape_google(self.url))


class BingEnum(GoogleEnum):
    """
    This class will make using of simple bing searches via bing dorks to enlist subdomains
    """

    def __init__(self, url) -> None:
        self.url = url
        self.GetDomain()

    def scrape_bing(self, query):
        query = urllib.parse.quote_plus(query)
        link = f'https://www.bing.com/search?q=site:{query}'
        response = GoogleEnum.ReturnSourceCode(self, link)
        # getting all the links from search result
        links = list(response.html.absolute_links)
        bing_domains = (

            'https://www.bing.com',
            'https://bing.com',
            'https://webcache.bing.com',
            'http://webcache.bing.com',
            'https://policies.bing.com',
            'https://support.bing.com',
            'https://maps.bing.com',
            'https://www.bing.com/maps'
        )

        for url in links[:]:
            if url.startswith(bing_domains):  # removing links with bing_domains in it
                links.remove(url)
                # self.subdomains=links # adding these links to our one universal list for keeping domains
        return links


class DuckDuckGoEnum(GoogleEnum):
    """
    This class will make using of simple duckduckgo searches via duckduckgo dorks to enlist subdomains
    """

    def __init__(self, url) -> None:
        self.url = url
      #  self.GetDomain()
        self.to_string()

    def scrape_duckduckgo(self, query):
        query = urllib.parse.quote_plus(query)
        link = f'https://www.duckduckgo.com/html/?q=site:{query}'
        response = GoogleEnum.ReturnSourceCode(self, link)
        # getting all the links from search result
        links = list(response.html.absolute_links)
        duckduckgo_domains = (

            'https://www.duckduckgo.com',
            'https://duckduckgo.com',
            'https://webcache.duckduckgo.com',
            'http://webcache.duckduckgo.com',
            'https://policies.duckduckgo.com',
            'https://support.duckduckgo.com',
            'https://maps.duckduckgo.com',
            'https://www.duckduckgo.com/maps',
            'https://html.duckduckgo.com'
        )

        for url in links[:]:
            # removing links with duckduckgo_domains in it
            if url.startswith(duckduckgo_domains):
                links.remove(url)
                # self.subdomains=links # adding these links to our one universal list for keeping domains
        return links

    def GetDomain(self):
        return GoogleEnum.GetUniqueDomains(self, self.scrape_duckduckgo(self.url))

    # function to convert list to string

    def to_string(self):
        print('\n'.join(self.GetDomain()))


class Shodan:
    """
    This class is using Shodan Search engine via a shodan API to enlist subdomains
    """
    api = shodan.Shodan(API_key)

    def __init__(self, url) -> None:
        self.url = url
        self.SearchDomains()

    def SearchDomains(self):
        r = requests.get(
            f'https://api.shodan.io/dns/domain/{self.url}?key={API_key}')
        data = json.loads(r.text)  # reading json data from return in r.text
        # load() and loads() for turning JSON encoded data into Python objects.
       # print(data)
        for item in data['data']:
            if item["subdomain"]!="":
                print(item['subdomain']+"."+self.url)


class Dictionary:
    """
    This takes a simple bruteforce approach towards subdomains finding by simply providing a input file
    """

    def __init__(self, url) -> None:
        self.url = url
        self.BruteForce()


    def read_file(self, path='./wordlist.txt'):
        # Opening file
        file = open(path, 'r')
        data = []
        for line in file:
            data.append(line.replace('\n', ""))
        # Closing files
        file.close()
        return data  # returns a list of subdomains from text file


    def req(self, subdomain):
        import urllib3
        http = urllib3.PoolManager()
        try:
                r = http.request('GET', f'http://{subdomain}.{self.url}')
                if r.status == 200:
                    print(f'{subdomain}.{self.url}')
                else:
                    pass
        except:
                pass


    def BruteForce(self):
        results = []
        with ThreadPoolExecutor(100) as executor:
            result=executor.map(self.req, self.read_file())
            print(result)

