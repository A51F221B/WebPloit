#import pyfiglet
import argparse
from rich import console
from SubdomainScanner.subdomains import Subdomains



c=console.Console() ## to beautify the console output we use rich print() function instead of defualt


class Argparse():
    """
    This class is used to parse the arguments from the command line
    """
    def __init__(self):
      description= "WebPloit - A Web Application Pentesting Framework"
      self.parser=argparse.ArgumentParser(c.print(description,style="bold red"),formatter_class=argparse.RawTextHelpFormatter)
      self.parser.add_argument("-s","--subdomains",help="Find Subdomains of a website",action="store",type=str)
      self.parser.add_argument("-a","--aggressive",help="Find Subdomains of a website",action="store_true")
      self.parser.add_argument("-u","--url",help="URL of the website",action="store",type=str)


    def validateURL(self,url):
      import re
      regex = "^((http|https)://)[-a-zA-Z0-9@:%._\\+~#?&//=]{2,256}\\.[a-z]{2,6}\\b([-a-zA-Z0-9@:%._\\+~#?&//=]*)$"
      r = re.compile(regex)
  
      if (re.search(r, url)):
          return True
      else:
          return False

    


def main():
  arg=Argparse()
  args=arg.parser.parse_args()

  # for subdomain enumeration
  if args.subdomains:
    if arg.validateURL(args.subdomains):
      if args.subdomains.startswith("http://"):
        args.subdomains=args.subdomains.replace("http://","") # removing http:// from the url
      if args.aggressive:
        Subdomains(args.subdomains,aggressive=True)
      else:
        Subdomains(args.subdomains,aggressive=False)
    else:
      c.print("[!] Invalid URL entered",style="bold red")
      c.print("[>] Example : example.com or http://example.com",style="bold green")

 
 
    

if __name__=='__main__':
    main()