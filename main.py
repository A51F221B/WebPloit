from subdomains import DuckDuckGoEnum, GoogleEnum,Shodan,BingEnum
#import pyfiglet
from rich import console
from rich.console import group
from rich.panel import Panel


c=console.Console() ## to beautify the console output we use rich print() function instead of defualt

class All():
    """
    This class inherits all other modules i.e. their classes
    
    """
    def __init__(self,url):
        self.url=url
        self.banner()
    
    def banner(self):
      #  text=pyfiglet.figlet_format("WebPloit") ## banner
        text="""
              __    ______ __       ____       
\ \      / /__| |__ |  _ \| | ___ (_) |_
 \ \ /\ / / _ \ '_ \| |_) | |/ _ \| | __|
  \ V  V /  __/ |_) |  __/| | (_) | | |_
   \_/\_/ \___|_.__/|_|   |_|\___/|_|\__|
"""
        c.print(text,style="bold red")


def main():
    c.print("[*] Enter a url : ")
    url = "google.com"
    All(url)        # example is facebook.com, google.com , Don't enter full url
    GoogleEnum(url)
    #Shodan(url)
    BingEnum(url)   # this will be used to get subdomains from bing
    DuckDuckGoEnum(url)
if __name__=='__main__':
    main()