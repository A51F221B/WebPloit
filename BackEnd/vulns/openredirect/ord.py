from ..FindingAnchorTags import Links
from SubdomainScanner.subdomains import *
import requests
import gevent.monkey
gevent.monkey.patch_all()


class OpenRedirect(Links):

    redirects = []

    def __init__(self, url):
        super().__init__(url)
      #  self.checklinks()
        # print(OpenRedirect.redirects)
        # print(self.checkredirects())

    def isRedirecting(self, urls):
        # keep allow_redirects= False to detect redirects
        r = requests.get(
            urls, headers={'User-agent': 'FireFox 101'}, allow_redirects=False)
        try:
            if str(r.status_code).startswith('3'):
                OpenRedirect.redirects.append(urls)
                return True, urls
            else:
                return False
        except:
            return False

    def checklinks(self):
        links = list(self.FindLinksInPage())
        print(links)
        # rs = (grequests.get(link) for link in links)
        # print(grequests.map(rs))
        for url in links:   
            print(self.isRedirecting(url))

        # print(self.redirects)

    def checkredirects(self):
        redirectUrl = []
        parameters = ['?next=', '?url=', '?uri=', '?r=', '?target=', '?rurl=', '?dest=', '?destination=',
                      '?redirect_url=', '?redir=', '?redirect=', '/redirect/', '?redirect_to=', '?return=', '?go=', '?target_url=']
        for p in parameters:
            for url in OpenRedirect.redirects:
                if p in url:
                    url = url.split('=')[0] + '='
                    redirectUrl.append(url)
        payload = "dtmkc"
        redirectUrl = [self.injectpayload(i, payload) for i in redirectUrl]
        return redirectUrl

    # lisf of places where openredirects occur are login,create password,reset,checkout
    # a method to inject payloads after parameters in the url

    def injectpayload(self, url, payload):
        # url = url.split('?')
        # url = url[0]+'?'+payload+'&'+url[1]
        return url + payload


# if __name__ == '__main__':
#     rd = OpenRedirect('https://fast.edu.pk/')
#     OpenRedirect.redirects = ['https://www.google.com?next=', 'https://www.bing.com?url=test.com',
#                               'https://www.yahoo.com?go=google.com', 'https://www.duckduckgo.com']
#    # print(rd.isRedirecting('https://mcdonalds.com.pk//wp-admin/'))
#     print(rd.checkredirects())


# http://s.adroll.com/j/exp/ERYIVUAW3VAMTPY6WYTWZX/index.js


class OpenSubs:

    def __init__(self, url):
        self.url = url
        Subdomains(url, aggressive=False)
      #  print(self.makepayload())
        self.request()

    def wordlist(self, path: str = "wordlist/openredirect.txt"):
        with open(path, "r") as file:
            data = []
            for line in file:
                data.append(line.replace("\n", ""))
        return data



    def makepayload(self):
        urls = []
        subdomains = list(set(Subdomains.subdomains))
        for subdomain in subdomains:
            for payloads in self.wordlist():
                url = 'http://'+subdomain+payloads
                urls.append(url)
        return urls


    def checkredirect(self, u):
        try:
            r = requests.get(u, allow_redirects=True)
            if str(r.status_code).startswith('3'):
                return u
            else:
                return r.status_code
        except:
            return False



    def request(self):
        url = list(set(self.makepayload()))
        for u in url:
            print(self.checkredirect(u))


# OpenSubs('fast.edu.pk')
