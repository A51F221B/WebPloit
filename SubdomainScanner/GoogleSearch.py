import requests
import urllib
from urllib.parse import urlparse
from requests_html import HTMLSession



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
        """
        Return the source code for the provided URL. 

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
                          'https://maps.google.',
                          'https://translate.google.com')

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
            exception = ['support.microsoft.com',
                         'go.microsoft.com', 'google.com']
        result = [i for n, i in enumerate(
            self.subdomains) if i not in self.subdomains[:n]]
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
