from .DuckSearch import DuckDuckGoEnum
from .ShodanSearch import Shodan
from .GoogleSearch import GoogleEnum
from .BingSearch import BingEnum
from .DictionarySearch import Dictionary



# Dictionary('nust.edu.pk')

class Subdomains(DuckDuckGoEnum):
    """
    This class will call functions from other classes to get unique subdomains
    """

    #subdomains = []

    def __init__(self, url, aggressive=False):
        self.url = url
        self.aggressive = aggressive
        self.GetSubdomains(aggressive)

    def GetSubdomains(self, aggressive):
       # Shodan(self.url)
        if self.aggressive:
            try:
                Shodan(self.url)
                Dictionary(self.url)
            except Exception as e:
                print(e)
        GoogleEnum(self.url)
        BingEnum(self.url)
        DuckDuckGoEnum(self.url)
        self.subdomains = DuckDuckGoEnum.GetDomain(self).copy()
        print(self.subdomains)


# if __name__ == '__main__':
#     Subdomains('jazz.com.pk', aggressive=False)
# print(type(DuckDuckGoEnum.GetDomain()))
