from requests_html import HTMLSession
from bs4 import BeautifulSoup as bs
import requests


session=HTMLSession()

class Links:
    def __init__(self,url) -> None:
        self.url=url
        self.FindLinksUsingBS()

    def FindLinksInPage(self): 
        url="https://au.edu.pk"
        response=session.get(url)
        links = response.html.absolute_links
        print(links)
    

    def FindLinksUsingBS(self):
        req=requests.get(self.url)
        soup = bs(req.text, 'html.parser')
        for link in soup.find_all('a'):
             print(link.get('href'))


Links("https://au.edu.pk")


    


        


