import re
import json
from rich import print_json
from .components import req
from .components import matcher
from .components.reader import Reader

class Scan:
    def __init__(self, url, template):
        self.url = url
        if not self.isValidUrl():
            print("Invalid URL")
            return
        self.template = template
        print_json(self.main())


    def main(self):
        r=Reader(self.template)
        # reader is returning the request data and the req method is using those and returning response data
        self.headers, self.payloads, self.method, self.redirects = r.reader()
        self.rdata,self.rbody = req.Requester(self.url, self.template, self.headers, self.payloads, self.method, self.redirects).req()
        # reader will now return matchers from the template
        self.matchtype, self.part, self.key, self.regex,self.code,self.matchCondition = r.readMatchers()
        # after getting the response we will pass this response data to matcher class
        _json=matcher.Matchers(self.matchCondition,self.matchtype,self.part,self.key,self.regex,self.code,self.payloads,self.rbody,self.rdata).forAPI()
        return json.dumps(_json, indent=4)
        

    def isValidUrl(self):
        regex = re.compile(
            r'^(?:http|ftp)s?://'  # http:// or https://
            r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+(?:[A-Z]{2,6}\.?|[A-Z0-9-]{2,}\.?)|'  # domain...
            r'localhost|'  # localhost...
            r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})'  # ...or ip
            r'(?::\d+)?'  # optional port
            r'(?:/?|[/?]\S+)$', re.IGNORECASE)
        
        return re.match(regex, self.url) is not None





# Scan("https://0a38006c04e66ad4c4b8e2d500c600dc.web-security-academy.net/product/stock","blueprints/xxe.json")
#Scan("http://ptl-3983322e-008445f2.libcurl.so/redirect.php?uri=","blueprints/openredirect.json")
