from requests_html import HTMLSession
from bs4 import BeautifulSoup as bs
import requests


session=HTMLSession()

class Links:
    def __init__(self,url) -> None:
        self.url=url

    def FindLinksInPage(self): 
        response=session.get(self.url)
        links = response.html.absolute_links
        return links
    

    def FindLinksUsingBS(self):
        req=requests.get(self.url)
        soup = bs(req.text, 'html.parser')
        for link in soup.find_all('a'):
             print(link.get('href'))










    


        


