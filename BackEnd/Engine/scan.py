from components.reader import Reader
from components import req
from components import matcher


class Scan:
    def __init__(self, url, template):
        self.url = url
        self.template = template
        r=Reader(self.template)
        # reader is returning the request data and the req method is usind those and returning response data
        self.headers, self.payloads, self.method, self.redirects = r.reader()
        self.rdata,self.rbody = req.Requester(self.url, self.template, self.headers, self.payloads, self.method, self.redirects).req()
       
        # reader will now return matchers from the template
        self.matchtype, self.part, self.key, self.regex,self.code,self.matchCondition = r.readMatchers()
        # after getting the response we will pass this response data to matcher class
        matcher.Matchers(self.matchCondition,self.matchtype,self.part,self.key,self.regex,self.code,self.payloads,self.rbody,self.rdata)

       





Scan("http://ptl-c7f2afd8-0eee6fd8.libcurl.so/redirect.php?uri=","blueprints/openredirect.json")

