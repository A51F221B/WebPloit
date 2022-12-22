import concurrent.futures
import requests
import socket
from rich.table import Table
from rich.console import Console
from rich.markdown import Markdown
from components.Search import *


class Subdomains:
    def __init__(self,url):
        self.url=url
        self.main()


    def get_http_status_code(self, domain):
        try:
            response = requests.get(f'http://{domain}',timeout=2)
            return response.status_code
        except:
            return 'N/A'


    def get_server(self, domain):
        try:
            response = requests.get(f'http://{domain}',timeout=2)
            server = response.headers['Server']
            return server
        except:
            return 'N/A'



    def process_subdomain(self, subdomain):
        ip_address = socket.gethostbyname(subdomain)
        code = self.get_http_status_code(subdomain)
        server = self.get_server(subdomain)

        output = (ip_address, str(code), subdomain, server)
        return output
    

    def main(self):
        from rich.live import Live
        console=Console()
        subdomains=Search(self.url).domains()

        # Create the table and add the headings
        table = Table(show_header=True, header_style="bold red")
        table.add_column("Ip address", style="dim", width=15)
        table.add_column("Code", style="dim", width=4)
        table.add_column("Subdomain", style="dim", width=35)
        table.add_column("Server", style="dim", width=30)

        with Live(table, refresh_per_second=3):
            for subdomain in subdomains:
                result = self.process_subdomain(subdomain)
                table.add_row(*result)



if __name__ == '__main__':
    Subdomains('jazz.com.pk')
