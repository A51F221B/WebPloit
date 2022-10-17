
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
        self.SearchDomains()
        print(self.listtoString())

    def SearchDomains(self):
        try:
            r = requests.get(
                f'https://api.shodan.io/dns/domain/{self.url}?key={API_key}')
            data = json.loads(r.text)
         #   print(json.dumps(data, indent=2))
            with open('Found_Subdomains.json', 'a') as f:
                f.write(json.dumps(data, indent=2))
                for subdomain in data['subdomains']:
                    self.subdomains.append(subdomain+'.'+self.url)
                return self.subdomains
        except Exception as e:
            print(e)

    def listtoString(self):
        return '\n'.join(self.subdomains)
