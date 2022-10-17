
import urllib
from urllib.parse import urlparse
from requests_html import HTMLSession
from .GoogleSearch import GoogleEnum


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
