from requests_html import HTMLSession
from bs4 import BeautifulSoup as bs
import requests


session=HTMLSession()

class Links:
    
    linkz=[]

    def __init__(self,url) -> None:
        self.url=url
        Links.linkz=list(self.FindLinksInPage())
       # print(Links.linkz)
        print(self.checkredirects())
      #  print(self.FindLinksInPage())

    def FindLinksInPage(self): 
        response=session.get(self.url)
        links = response.html.absolute_links
        return links
    

    def FindLinksUsingBS(self):
        req=requests.get(self.url)
        soup = bs(req.text, 'html.parser')
        for link in soup.find_all('a'):
             print(link.get('href'))


    def checkredirects(self):
      #  urls=list(self.FindLinksInPage())
        redirectUrl = []
        parameters = ['?next=', '?url=', '?uri=', '?r=', '?target=', '?rurl=', '?dest=', '?destination=',
                      '?redirect_url=', '?redir=', '?redirect=', '/redirect/', '?redirect_to=', '?return=', '?go=', '?target_url=','?success_redirect_url']
        for p in parameters:
            for url in Links.linkz:
                if p in url:
                    url = url.split('=')[0] + '='
                    redirectUrl.append(url)
        # payload = "dtmkc"
        # redirectUrl = [self.injectpayload(i, payload) for i in redirectUrl]
        return redirectUrl


    # finding xss endpoints in links


Links('https://au.edu.pk')






    


        


