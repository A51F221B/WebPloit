from tkinter.messagebox import RETRY
import gevent.monkey
gevent.monkey.patch_all()
import requests
from FindingAnchorTags import Links
import grequests

class OpenRedirect(Links):
    
    redirects=[]
    def __init__(self, url):
        super().__init__(url)
      #  self.checklinks()
      #  print(self.isRedirecting())
       

    def isRedirecting(self,urls):
        r=requests.get(urls,headers={'User-agent':'FireFox 101'},allow_redirects=False) # keep allow_redirects= False to detect redirects
        try:
            if str(r.status_code).startswith('3'):
                self.redirects.append(urls)
                return True,urls
            else:
                return False
        except:
            return False


    def checklinks(self):
        links=list(self.FindLinksInPage())
        print(links)
        # rs = (grequests.get(link) for link in links)
        # print(grequests.map(rs))
        for url in links:
            print(self.isRedirecting(url))
        #print(self.redirects)

    
    def checkredirects(self):
        redirectUrl=[]
        parameters=['?next=','?url=','?uri=','?r=','?target=','?rurl=','?dest=','?destination=',
            '?redirect_url','?redir=','?redirect','/redirect/','?redirect_to','?return','?go=','?target_url=']
        for p in parameters:
            for url in self.redirects:
                if p in url:
                    redirectUrl.append(url)
        return redirectUrl

    # lisf of places where openredirects occur are login,create password,reset,checkout



if __name__=='__main__':
    rd=OpenRedirect('https://fast.edu.pk/')
  #  rd.redirects = ['https://www.google.com?next=', 'https://www.bing.com?url=test.com', 'https://www.yahoo.com?go=google.com', 'https://www.duckduckgo.com']
   # print(rd.isRedirecting('https://mcdonalds.com.pk//wp-admin/'))




#http://s.adroll.com/j/exp/ERYIVUAW3VAMTPY6WYTWZX/index.js