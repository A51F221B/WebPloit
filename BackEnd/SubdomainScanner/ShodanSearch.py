
import requests
import json
import shodan 
from API.config import API_key



class Shodan:
    """
    This class is using Shodan Search engine via a shodan API to enlist subdomains
    """
    api = shodan.Shodan(API_key)
    
    subdomains = []

    def __init__(self, url) -> None:
        self.url = url
        print(self.listtoString())

    def SearchDomains(self):
        try:
            r = requests.get('https://api.shodan.io/dns/domain/'+self.url+'?key='+API_key)
            data = json.loads(r.text)
            return data
        except Exception as e:
            pass


    def listtoString(self):
        try:
            data=self.SearchDomains()
            for subdomain in data['subdomains']:
                self.subdomains.append(subdomain+'.'+self.url)
            return '\n'.join(self.subdomains)
        except Exception as e:
            pass


    def writeToFile(self):
        with open('Found_Subdomains.json', 'w') as f:
            f.write(json.dumps(self.SearchDomains(), indent=2))

