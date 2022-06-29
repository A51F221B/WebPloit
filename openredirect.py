import requests



class OpenRedirect:
    
    def __init__(self,url):
        self.url=url
        r=requests.get(url)
    
    def isRedirecting(self,url):
        try:
            if str(self.r.status_code).startswith('3'):
                return True
            else:
                return False
        except:
            return False


    def getRedirectedUrl(self):
        if(self.isRedirecting(self.url)):
            return self.r.headers['Location']
        return False



rd=OpenRedirect("https://au.edu.pk")
print(rd.getRedirectedUrl())
