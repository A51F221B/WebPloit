import subdomains
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
    
    def banner(self):
        text=pyfiglet.figlet_format("WebPloit") ## banner
        c.print(text,style="bold red")

    def UserInput(self):
        c.print("[*] Enter a url : ")
        url=input()
     #   subdomains.Dictionary.FindDomain(self,url)
       # print(subdomains.GoogleEnum.FinalDomains(self,url))
        obj=subdomains.GoogleEnum()
        print(obj.GetDomain(url))
      #  test=subdomains.GoogleEnum.GetDomain(url)
       # print(test)

def main():
    main=All()
    main.banner()
    main.UserInput()


if __name__=='__main__':
    main()