from rich import console
from threading import Thread, Lock
from queue import Queue



class Dictionary:
    """
    This class uses a wordlist of subdomains and checks if the subdomains are available or not
    Threading is being used in this class
    """
    c = console.Console()

    def __init__(self, url):
        self.url = url
        self.q = Queue()
        self.found = Queue()
        self.thread_Lock = Lock()
        self.init()

    # method to return list from text file
    def wordlist(self, path: str = "wordlist/wordlist.txt"):
        with open(path, "r") as file:
            data = []
            for line in file:
                data.append(line.replace("\n", ""))
        return data

    def scan(self, subdomain):
        import urllib3
        http = urllib3.PoolManager()
        try:
            r = http.request(
                'GET',
                f'https://{subdomain}.{self.url}',
                redirect=True,
                timeout=3
            )

            if r.status == 200:
                with self.thread_Lock:
                    self.c.print(
                        f'[+] {subdomain}.{self.url}', style="bold green")
                    self.found.append(subdomain)
            elif r.status == 503:
                with self.thread_Lock:
                    self.c.print(
                        f'[-] {subdomain}.{self.url} ', style="bold green")
            else:
                with self.thread_Lock:
                    self.c.print(
                        f'[-] {subdomain}.{self.url}', style="bold red")
        except Exception as e:
         #   print(f"Error occurred: {e}")
            pass

    def extract(self):
        while True:
            try:
                subdomain = self.q.get()
                self.scan(subdomain)
                self.q.task_done()
            except KeyboardInterrupt:
                exit(1)
            except Exception as E:
                print("Error occurred: {}".format(E))

    def init(self, threads=100):
        subdomain = self.wordlist()
        try:
            for thread in range(threads):
                thread = Thread(target=self.extract)
                thread.daemon = True
                thread.start()
            for subdomain in subdomain:
                self.q.put(subdomain)

            self.q.join()

        except KeyboardInterrupt:
            print("CTRL+C detected!")

