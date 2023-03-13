import requests
from .API.config import SHODAN_API_key
from .API.config import VIRUSTOTAL_API



class Shodan:
    def __init__(self,url):
        self.url=url
       # print(self.shodan_search())
      #  print(self.virus_total())


    def shodan_search(self,api=SHODAN_API_key):
        # use Shodan API to search for subdomains and return a list of subdomains
        subdomains = []
        try:
           r = requests.get('https://api.shodan.io/dns/domain/'+self.url+'?key='+api)
           subdomains = r.json()['subdomains'] 
        except Exception as e:
            return []
        return subdomains


    def virus_total(self, api=VIRUSTOTAL_API):
        try:
            response=requests.get(f'https://www.virustotal.com/vtapi/v2/domain/report?apikey={api}&domain={self.url}')
            response=response.json()
            subdomains=response['subdomains']
            return subdomains
        except Exception as e:
            return []




