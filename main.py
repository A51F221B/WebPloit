from subdomains import GoogleEnum
import pyfiglet
from rich import console,status
from rich.console import group
from rich.panel import Panel
import threading

c=console.Console() ## to beautify the console output we use rich print() function instead of defualt

class All():
    """
    This class inherits all other modules i.e. their classes
    
    """
    def __init__(self,url):
        self.url=url
        self.banner()
    
    def banner(self):
        text=pyfiglet.figlet_format("WebPloit") ## banner
        c.print(text,style="bold red")


def main():
    c.print("[*] Enter a url : ")
    url = "au.edu.pk"
    All(url)
    GoogleEnum(url)


if __name__=='__main__':
    main()