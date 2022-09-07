import json
import re
import urllib3
from queue import Queue
from threading import Thread,Lock




class Fuzzer:
    """
    Only God knows how this code works
    """


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
            self.req()
        elif data['request']['payloads']==False:
            f=Fuzzer(self.url)


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
        flag=False 
        #try:
        for matcher in data['matches']:
            if matcher['type']=='status':
                for code in matcher['status']:
                    if status==code:
                        flag=True
    
                
        
        if matcher['type']=='body':
            print(matcher['type'])
        
        if matcher['type']=='regex':
            if matcher['part']=='header':
                pass
        # except:
        #     pass    



    def status(self):
        pass



    

#fuff=Fuzzer('http://au.edu.pk','vulns/templates/openredirect.json')
engine=Engine('https://au.edu.pk','vulns/templates/openredirect.json')

    

    