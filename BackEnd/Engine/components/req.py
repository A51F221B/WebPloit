import urllib3


class Requester:
    def __init__(self,url,template,headers,payloads,method,redirects):
        self.url = url
        self.template = template
        self.headers = headers
        self.payloads = payloads
        self.method = method
        self.redirects = redirects


    def req(self):
        # using urllib3 to send requests
        http = urllib3.PoolManager()
        responses = {}
        try:
            if self.method == "GET":
                for payload in self.payloads:
                    full_url = f"{self.url}{payload}"
                    response = http.request('GET', full_url, headers=self.headers, redirect=self.redirects)
                    # Convert the HTTPHeaderDict object to a dictionary before adding it to the responses
                    responses[payload] = {"headers": dict(response.headers.items()), "status": response.status, "data": response.data}
            elif self.method == "POST":
                pass
        except urllib3.exceptions.MaxRetryError as e:
            # Handle MaxRetryError exceptions here
            print("An error occurred:", e)
        except urllib3.exceptions.SSLError as e:
            # Handle SSLError exceptions here
            print("An SSL error occurred:", e)
        except urllib3.exceptions.RequestError as e:
            # Handle RequestError exceptions here
            print("A request error occurred:", e)
        except urllib3.exceptions.TimeoutError as e:
            # Handle TimeoutError exceptions here
            print("The request timed out:", e)
        except urllib3.exceptions.ProtocolError as e:
            # Handle ProtocolError exceptions here
            print("A protocol error occurred:", e)
        except urllib3.exceptions.DecodeError as e:
            # Handle DecodeError exceptions here
            print("An error occurred while decoding the response:", e)
        except urllib3.exceptions.SSLError as e:
            print("An SSL certificate verification error occurred:", e.reason)

        except Exception as e:
            # Handle any other exceptions here
            print("An unknown error occurred:", e)
        # return responses and body
        return responses, response.data




