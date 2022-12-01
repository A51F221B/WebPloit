#!/usr/bin/env python3
from .core import requester
from .core.extractor import Extractor
from .core import save_it
from .core import anchortags
from urllib.parse import unquote 
import requests
import re
import argparse
import os
import sys
import json
import time 
start_time = time.time()


def init(domain,subs,level,exclude,output,placeholder,quiet,retries,vulns):

    if subs == True or " True":
        url = f"https://web.archive.org/cdx/search/cdx?url=*.{domain}/*&output=txt&fl=original&collapse=urlkey&page=/"
    else:
        url = f"https://web.archive.org/cdx/search/cdx?url={domain}/*&output=txt&fl=original&collapse=urlkey&page=/"
    
    alist=anchortags.FindLinksInPage(f'https://{domain}')

    retry = True
    retries = 0
    while retry == True and retries <= int(retries):
             response, retry = requester.connector(url)
             retry = retry
             retries += 1
    if response == False:
         return
    response = unquote(response) # to decode the url
   
    # for extensions to be excluded 
    black_list = []
    if exclude:
         if "," in exclude:
             black_list = exclude.split(",")
             for i in range(len(black_list)):
                 black_list[i] = "." + black_list[i]
         else:
             black_list.append("." + exclude)
             
    else: 
         black_list = [] # for blacklists
    if exclude:
        print(f"\u001b[31m[!] URLS containing these extensions will be excluded from the results   : {black_list}\u001b[0m\n")
    

    global final_uris
    final_uris=[]
    ex=Extractor()
    final_uris = ex.param_extract(response , level , black_list, placeholder)
    final_uris.extend(alist)
    final_uris = list(set(final_uris))

   
    # variable final_urls is the final list of urls that are extracted

  #  save_it.save_func(final_uris , args.output , args.domain)

    if not quiet:
        print("\u001b[32;1m")
        print('\n'.join(final_uris))
        print("\u001b[0m")

    print(f"\n\u001b[32m[+] Total number of retries:  {retries-1}\u001b[31m")
    print(f"\u001b[32m[+] Total unique urls found : {len(final_uris)}\u001b[31m")
    # if args.output:
    #     if "/" in args.output:
    #         print(f"\u001b[32m[+] Output is saved here :\u001b[31m \u001b[36m{args.output}\u001b[31m" )

    #     else:
    #         print(f"\u001b[32m[+] Output is saved here :\u001b[31m \u001b[36moutput/{args.output}\u001b[31m" )
    # else:
    #     print(f"\u001b[32m[+] Output is saved here   :\u001b[31m \u001b[36moutput/{args.domain}.txt\u001b[31m")
    print("\n\u001b[31m[!] Total execution time      : %ss\u001b[0m" % str((time.time() - start_time))[:-12])

    if vulns:
        data=readFile(vulns)
        print(f"\u001b[32m[+] Potential endpoints for {vulns} are :\u001b[31m")
        ex=Extractor()
        print(ex.find_strings(final_uris,data["patterns"]))
    




def readFile(file):
    paths={
        "openredirect":"EndpointsParser/profiles/redirect.json",
        "xss":"EndpointsParser/profiles/xss.json",
    }
    with open(paths[file]) as json_file:
        data = json.loads(json_file.read())
        return data



# if __name__ == "__main__":
#     main()
#     ex = Extractor()
#     readFile("profiles/potential.json")
#     print(data["patterns"])

#     print("Redirecting urls are : ")
    
#     parameters = ['?next=', '?url=', '?uri=', '?r=', '?target=', '?rurl=', '?dest=', '?destination=','?redirect_url=', '?redir=', '?redirect=', '/redirect/', '?redirect_to=', '?return=', '?go=', '?target_url=','?success_redirect_url']


#     print(ex.find_strings(final_uris, data["patterns"]))




