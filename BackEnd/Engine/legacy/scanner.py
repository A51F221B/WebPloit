import json
import re
import urllib3
from queue import Queue
from threading import Thread, Lock


class WebBody:
    status_code: int = 500
    content: str = ""
    headers: dict = {}

    def __init__(self, status_code="", content="", headers=""):
        self.status_code = status_code
        self.content = content
        self.headers = headers


web_body = WebBody()


class Fuzzer:

    def __init__(self, url):
        self.url = url
        # self.file = file
        # self.readFile()
        self.q = Queue()
        self.found = Queue()
        self.thread_Lock = Lock()
        self.init()

  
  
    def scan(self, payload):
        global responseheaders, status, responsebody
        http = urllib3.PoolManager()
        url = f'{self.url}/{payload}', #note that this is just url variable and is just being printed
        try:
            r = http.request(
                data['request']['method'],
                url=f'{self.url}{payload}', # if we want url/payload add "/payload" in json template
                headers=data['request']['headers'],
                redirect=data['request']['redirects']
            )
        except:
            pass
        print(f'{url} {r.status}')
        responseheaders = r.headers
        # print(responseheaders)
        responsebody = r.data
        status = r.status
        self.checkers()

  
    
    def checkers(self):
        global regmatch
        flag = False
        # try:
        for matcher in data['matches']:
            if matcher['type'] == 'status':
                for code in matcher['status']:
                    if status == code:
                        flag = True
                        # print(f"Status Code : {flag}")
                        web_body.status_code = flag

            if matcher['type'] == 'body':
                pass

            if matcher['type'] == 'regex':
               # print(data['id'])
                if matcher['part'] == 'header':
                    if matcher['key'] in responseheaders:
                        head = f'{matcher["key"]}: {responseheaders[matcher["key"]]}'
                        print(head)
                        reg=matcher['regex'] # uncomment this if you want to use regex from json file
                        #reg=r"(?m)^(?:Server\s*?:\s*?)(?:https?:\/\/|\/\/|\/\\\\|\/\\)?(?:[a-zA-Z0-9\-_\.@]*)cloudflare\/?(\/|[^.].*)?$"
                        # reg = r"(?m)^(?:Location\s*?:\s*?)(?:https?:\/\/|\/\/|\/\\\\|\/\\)?(?:[a-zA-Z0-9\-_\.@]*)example\.com\/?(\/|[^.].*)?$"
                        try:
                            regmatch = Fuzzer.regex_match(self, reg, head)
                            print(f"Pattern found : {regmatch}")
                        except:
                            pass

                if matcher['part'] == 'body':
                   # print(responsebody)
                    reg = matcher['regex']
                    print(reg)
                    b = responsebody.decode('utf-8')
                    regmatch = Fuzzer.regex_match(self, reg, b)
                    print(f"Pattern found : {regmatch}")
        try:
            self.matchersCondition(flag, regmatch)
            # if(self.matchersCondition(flag, regmatch)) and data["stopAtMatch"]==True:
            #     exit(1)
        except Exception as e:
            pass
     

    def printinfo(self):
        # returning vulnerability information in json format 
        return {
            "id": data['id'],
            "endpoint": self.url,
            "request": data['request'],
            "matches": data['matches']
        }




    def matchersCondition(self, flag, regmatch):
        import pprint
        if data['matchers-condition'] == 'and':
            if flag and regmatch:
                print("Vulnerability Found")
                pprint.pprint(self.printinfo())
                return True
            else:
                print("Vulnerability not found")
                return False
        elif data['matchers-condition'] == 'or':
            if flag or regmatch:
                print("Vulnerability Found")
                pprint.pprint(self.printinfo())
                return True



  
    def extract(self):
        while True:
            try:
                payload = self.q.get()
                self.scan(payload)
                self.q.task_done()
            except KeyboardInterrupt:
                exit(1) 
            except Exception as E:
                print("Error occurred: {}".format(E))

  
  
    def readFile(self):
        global data
        with open(self.file) as json_file:
            data = json.loads(json_file.read())
            return data

  
  
    def init(self, threads=100):
        try:
            for thread in range(threads):
                thread = Thread(target=self.extract)
                thread.daemon = True
                thread.start()
            for p in data['payloads']:
                self.q.put(p)

            self.q.join()

        except KeyboardInterrupt:
            print("CTRL+C detected!")



    def regex_match(self, regex, string):
        matches = re.finditer(regex, string, re.MULTILINE | re.IGNORECASE)
        for match in matches:
            return True
        return False





class Engine(Fuzzer):

    def __init__(self, url, file):
        self.url = url
        self.file = file
        self.readFile()
      #  self.req()
      #  print(self.match())
       # self.status()

  
  
    def start(self):
        self.request()

  
  
    def request(self):
        if data['request']['payloads'] == True:
            f = Fuzzer(self.url)
        elif data['request']['payloads'] == False:
            self.req()

  
  
    def req(self):
        global status, responseheaders, flag, responsebody

        # body = '''<?xml version="1.0" encoding="UTF-8"?><!DOCTYPE test [ <!ENTITY xxe SYSTEM "file:///etc/passwd"> ]><stockCheck><productId>&xxe;</productId><storeId>1</storeId></stockCheck>'''

        http = urllib3.PoolManager()
        print(f"payloads : {data['request']['payloads']}")
        if data['request']['method'] == 'GET':
            r = http.request(
                data['request']['method'],
                url=self.url,
                headers=data['request']['headers'],
                redirect=data['request']['redirects'],
            )

        elif data['request']['method'] == 'POST':
            r = http.request(
                data['request']['method'],
                url=self.url,
                headers=data['request']['headers'],
                #body=body
                body=data['request']['body']
            )
      #  print(r.headers)
        status = r.status
        responseheaders = r.headers
        responsebody = r.data
        print(status)
        print(responseheaders)
        print(r.data)
        self.checkers()



def start(url):
    files = [
        'vulns/blueprints/openredirect.json',
        'vulns/blueprints/xxe.json'
        'vulns/blueprints/xss.json'
    ]
    for file in files:
        Engine(url, file).start()



ATTACK_FILE = {
    "xxe" : 'vulns/blueprints/xxe.json',
    "open_redirect" : 'vulns/blueprints/openredirect.json',
    "xss" : 'vulns/blueprints/xss.json'
}


def start(url, attack_type):
        Engine(url, ATTACK_FILE[attack_type]).start()
        return status, responseheaders, responsebody



# # fuff=Fuzzer('http://au.edu.pk','vulns/templates/openredirect.json')
# engine = Engine('http://ptl-30929a59-df95151f.libcurl.so/redirect.php?uri=https://example.com','blueprints/openredirect.json').start()


# https://ptl-b00d72f4-cf435e49.libcurl.so/redirect.php?uri=https://example.com


