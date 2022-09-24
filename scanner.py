import json
import re
import urllib3
from queue import Queue
from threading import Thread,Lock




class Fuzzer:


    def __init__(self,url):
        self.url = url
        # self.file = file
        # self.readFile()
        self.q = Queue()
        self.found = Queue()
        self.thread_Lock = Lock()
        self.init()



    def scan(self, payload):
        global responseheaders,status
        http=urllib3.PoolManager()
        url=f'{self.url}/{payload}',
        r=http.request(
            data['request']['method'],
            url=f'{self.url}/{payload}',
            headers=data['request']['headers'],
            redirect=data['request']['redirects']
        )
        print(f'{url} {r.status}')
        responseheaders=r.headers
        #print(responseheaders)
        status=r.status
        self.checkers()
        


    def checkers(self):
        flag=False 
        #try:
        for matcher in data['matches']:
            if matcher['type']=='status':
                for code in matcher['status']:
                    if status==code:
                        flag=True
                        print(f"Status Code : {flag}")
    
        
            if matcher['type']=='body':
                pass
                    
            if matcher['type']=='regex':
               # print(data['id'])
                if matcher['part']=='header':
                    if matcher['key'] in responseheaders:
                        head=f'{matcher["key"]}: {responseheaders[matcher["key"]]}'
                        print(head)
                        #reg=r"(?m)^(?:Server\s*?:\s*?)(?:https?:\/\/|\/\/|\/\\\\|\/\\)?(?:[a-zA-Z0-9\-_\.@]*)cloudflare\/?(\/|[^.].*)?$"
                        reg=r"(?m)^(?:Location\s*?:\s*?)(?:https?:\/\/|\/\/|\/\\\\|\/\\)?(?:[a-zA-Z0-9\-_\.@]*)example\.com\/?(\/|[^.].*)?$"
                        regmatch=Engine.regex_match(self,reg,head)
                        print(f"Pattern found : {regmatch}")
        self.matchersCondition(flag,regmatch)



    def matchersCondition(self,flag,regmatch):
        if data['matchers-condition'] == 'and':
            if flag and regmatch:
                print("Vulnerability Found")
                return True
            else:
                print("Vulnerability not found")
                return False
        elif data['matchers-condition'] == 'or':
            if flag or regmatch:
                print("Vulnerability Found")
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





class Engine(Fuzzer):

    def __init__(self,url,file):
        self.url=url
        self.file=file
        self.readFile()
      #  self.req()
      #  print(self.match())
       # self.status()
        self.request()


    def request(self):
        if data['request']['payloads']==True:
            f=Fuzzer(self.url)
        elif data['request']['payloads']==False:
            self.req()


    def req(self):
        global status,responseheaders,flag

        #body='''<?xml version="1.0" encoding="UTF-8"?><!DOCTYPE test [ <!ENTITY xxe SYSTEM "file:///etc/passwd"> ]><stockCheck><productId>&xxe;</productId><storeId>1</storeId></stockCheck>'''
        
        http=urllib3.PoolManager()
        print(f"payloads : {data['request']['payloads']}")
        if data['request']['method']=='GET':
                r=http.request(
                data['request']['method'],
                url=self.url,
                headers=data['request']['headers'],
                redirect=data['request']['redirects'],
            )
        

        elif data['request']['method']=='POST':
            r=http.request(
                data['request']['method'],
                url=self.url,
                headers=data['request']['headers'],
                body=data['request']['body']
            )
      #  print(r.headers)
        status=r.status
        print(status)
        responseheaders=r.headers
        print(responseheaders)
        print(r.data)
       # self.checkers()
 

    def regex_match(self,regex, string):
        matches = re.finditer(regex, string, re.MULTILINE | re.IGNORECASE)
        for match in matches:
            return True
        return False




    

#fuff=Fuzzer('http://au.edu.pk','vulns/templates/openredirect.json')
engine=Engine('https://0a8500b80342dbe7c064220400ac0080.web-security-academy.net/product/stock','vulns/templates/xxe.json')

    

# https://ptl-b00d72f4-cf435e49.libcurl.so/redirect.php?uri=https://example.com


