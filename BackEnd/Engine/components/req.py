import urllib3
from urllib.parse import urlparse

class Requester:
    def __init__(self,url,template,headers,payloads,method,redirects):
        self.url = url
        self.template = template
        self.headers = headers
        self.payloads = payloads
        self.method = method
        self.redirects = redirects

    def req(self):
        http = urllib3.PoolManager()
        responses = {}

        for payload in self.payloads:
            try:
                if self.method == "GET":
                    full_url = f"{self.url}{payload}"
                    print(full_url)
                    try:
                        response = http.request('GET', full_url, headers=self.headers, redirect=self.redirects, timeout=10)
                    except urllib3.exceptions.MaxRetryError as e:
                        http = urllib3.PoolManager(cert_reqs='CERT_NONE')
                        response = http.request('GET', full_url, headers=self.headers, redirect=self.redirects, timeout=10)

                elif self.method == "POST":
                    p = urlparse(self.url)
                    hostname = p.hostname
                    self.headers['Host'] = hostname

                    try:
                        response = http.request('POST', self.url, headers=self.headers, body=payload, redirect=self.redirects, timeout=10)
                    except urllib3.exceptions.MaxRetryError as e:
                        http = urllib3.PoolManager(cert_reqs='CERT_NONE')
                        response = http.request('POST', self.url, headers=self.headers, body=payload, redirect=self.redirects, timeout=10)

                responses[payload] = {"headers": dict(response.headers.items()), "status": response.status, "data": response.data}

            except urllib3.exceptions.MaxRetryError as e:
                pass
            except urllib3.exceptions.SSLError as e:
                print("An SSL error occurred:", e)
            except urllib3.exceptions.RequestError as e:
                print("A request error occurred:", e)
            except urllib3.exceptions.TimeoutError as e:
                print("The request timed out:", e)
            except urllib3.exceptions.ProtocolError as e:
                print("A protocol error occurred:", e)
            except urllib3.exceptions.DecodeError as e:
                print("An error occurred while decoding the response:", e)
            except urllib3.exceptions.SSLError as e:
                print("An SSL certificate verification error occurred:", e.reason)
            except Exception as e:
                print("An unknown error occurred:", e)

        try:
            return responses, response.data
        except:
            return responses, None
