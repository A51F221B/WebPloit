import argparse
from rich import console
from rich.console import group
from rich.panel import Panel
import tabulate as tb
import sys
from SubdomainScanner.subdomains import Subdomains


c=console.Console() ## using the rich print() instead of default print() function

"""
providing a cli interface for the backend
it will contain options like info,help,set subdomains,set url,set vuln,exit
forexample : Webploit > set subdomains
            Webploit > set url
"""


class CLI:
    def __init__(self):
        self.main()

    def info(self):
        c.print("WebPloit - A Web Application Pentesting Framework",style="bold red")
        c.print("Author : Asif Masood (A51F221B)",style="bold green")
        c.print("Version : 0.1",style="bold red")


    def set_subdomains(self):
        c.print("Enter the domain name (url) to find its subdomains",style="bold green")
        c.print("WebPloit > ",end="",style="bold red")
        domain=input()
        global d
        d=domain
        c.print("Do you want to use aggressive mode? (y/n)",style="bold green")
        c.print("WebPloit > ",end="",style="bold red")
        mode=input()
        if mode=="y":
            Subdomains(domain,aggressive=True)
        elif mode=="n":
            Subdomains(domain,aggressive=False)
        else:
            c.print("Invalid Command",style="bold red")



    def help(self):
        table=[["info","Show information about the framework"],["help","Show help menu"],["set subdomain","Set the domain to find its subdomains"],["set url","Set the url to find its subdomains"],["set vuln","Set the vulnerability to find its subdomains"],["show options","Show the options already set"],["exit","Exit the framework"]]
        c.print(tb.tabulate(table,headers=["Command","Description"]),style="bold white")



    def showAlreadySetOptions(self):
        options=[["Subdomain"],["URL"],["Vulnerability"]]
        c.print(tb.tabulate(options,headers=["Options"]),style="bold white")
    
    

    def main(self):
        while True:
            c.print("WebPloit > ",end="",style="bold green")
            command=input()
            if command=="show info":
                self.info()
            elif command=="show help":
                self.help()
            elif command=="set subdomain":
                # if user enters set subdomains https://example.com get the string example.com
                command=command.strip("set subdomain ")
                print(command)
               # self.set_subdomains()
            elif command=="set url":
                self.set_url()
            elif command=="set vuln":
                self.set_vuln()
            elif command=="exit":
                exit(1)
            elif command=="show options":
                self.showAlreadySetOptions()
            elif command=="":
                pass
            elif command == "clear":
                c.clear()
            else:
                c.print("Invalid Command",style="bold red")
    

if __name__=="__main__":
    cli=CLI()