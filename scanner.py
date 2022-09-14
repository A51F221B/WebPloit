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
        global responseheaders,rstatus
        http=urllib3.PoolManager()
        r=http.request(
            data['request']['method'],
            url=self.url,
            headers=data['request']['headers'],
            redirect=data['request']['redirects']
        )
        url=f'{self.url}/{payload}',
        print(f'{url} {r.status}')
        responseheaders=r.headers
        rstatus=r.status



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

        http=urllib3.PoolManager()
        print(f"payloads : {data['request']['payloads']}")
        r=http.request(
            data['request']['method'],
            url=self.url,
            headers=data['request']['headers'],
            redirect=data['request']['redirects']
        )
      #  print(r.headers)
        status=r.status
        print(status)
        responseheaders=r.headers
       # print(responseheaders)
        flag=False 
        #try:
        for matcher in data['matches']:
            if matcher['type']=='status':
                for code in matcher['status']:
                    if status==code:
                        flag=True
    
        
            if matcher['type']=='body':
                print("This is the body part")
                    
            if matcher['type']=='regex':
                print(data['id'])
                if matcher['part']=='header':
                    if matcher['key'] in responseheaders:
                        head=f'{matcher["key"]}: {responseheaders[matcher["key"]]}'
                        print(head)
                        reg=r"(?m)^(?:Server\s*?:\s*?)(?:https?:\/\/|\/\/|\/\\\\|\/\\)?(?:[a-zA-Z0-9\-_\.@]*)cloudflare\/?(\/|[^.].*)?$"
                        print(self.regex_match(reg,head))
        
        # except:
        #     pass    



    def status(self):
        pass

    def regex_match(self,regex, string):
        matches = re.finditer(regex, string, re.MULTILINE | re.IGNORECASE)
        for match in matches:
            return True
        return False




    

#fuff=Fuzzer('http://au.edu.pk','vulns/templates/openredirect.json')
engine=Engine('https://au.edu.pk','vulns/templates/openredirect.json')

    

    