from .DuckSearch import DuckDuckGoEnum
from .ShodanSearch import Shodan
from .GoogleSearch import GoogleEnum
from .BingSearch import BingEnum
from .DictionarySearch import Dictionary
import json


# Dictionary('nust.edu.pk')

class Subdomains(DuckDuckGoEnum):
    """
    This class will call functions from other classes to get unique subdomains
    """

    #subdomains = []

    def __init__(self, url, aggressive=False):
        self.url = url
        self.aggressive = aggressive
        self.GetSubdomains()


    def GetSubdomains(self):
        if self.aggressive:
            try:
                print(Dictionary(self.url))
            except Exception as e:
                print(e)
        Shodan(self.url)
        GoogleEnum(self.url)
        BingEnum(self.url)
        DuckDuckGoEnum(self.url)
        self.subdomains = DuckDuckGoEnum.GetDomain(self).copy()
    
    def toJson(self):
        return json.dumps(self.subdomains, indent=2)


# if __name__ == '__main__':
#     Subdomains('jazz.com.pk', aggressive=False)
# print(type(DuckDuckGoEnum.GetDomain()))
