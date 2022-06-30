import requests
from FindingAnchorTags import Links


class OpenRedirect(Links):
    def __init__(self, url):
        super().__init__(url)
        self.checklinks()

    def isRedirecting(self):
        r=requests.get(self.url)
        try:
            if str(r.status_code).startswith('3'):
                return True
            else:
                return False
        except:
            return False


    def checklinks(self):
        links=list(self.FindLinksInPage())
        print(links)
        # for link in links:
        #     print(self.isRedirecting())



    def getRedirectedUrl(self):
        if(self.isRedirecting(self.url)):
            return self.r.headers['Location']
        return False


if __name__=='__main__':
    rd=OpenRedirect('https://au.edu.pk')

