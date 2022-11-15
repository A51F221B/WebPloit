import urllib
from urllib.parse import urlparse
from requests_html import HTMLSession
from .GoogleSearch import GoogleEnum


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
