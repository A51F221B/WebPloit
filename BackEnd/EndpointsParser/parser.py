#!/usr/bin/env python3
from .core import requester
from .core.extractor import Extractor
from .core import save_it
from .core import anchortags
from urllib.parse import unquote 
import json
import time 
start_time = time.time()


def init(domain,subs=None,level=None,exclude=None,output=None,placeholder=None,quiet=None,retries=None,vulns=None):

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
    

    # variable final_urls is the final list of urls that are extracted
    global final_uris
    final_uris=[]
    ex=Extractor()
    final_uris = ex.param_extract(response , level , black_list, placeholder)
    final_uris.extend(alist)
    final_uris = list(set(final_uris))

    if not quiet:
        print("\u001b[32;1m")
        print('\n'.join(final_uris))
        print("\u001b[0m")

    print(f"\n\u001b[32m[+] Total number of retries:  {retries-1}\u001b[31m")
    print(f"\u001b[32m[+] Total unique urls found : {len(final_uris)}\u001b[31m")
    print("\n\u001b[31m[!] Total execution time      : %ss\u001b[0m" % str((time.time() - start_time))[:-12])

    if vulns:
        data=readFile(vulns)
        print(f"\u001b[32m[+] Potential endpoints for {vulns} are :\u001b[31m")
        ex=Extractor()
        vulnurl=ex.find_strings(final_uris,data["patterns"])
        # red color
        print("\u001b[31m")
        print('\n'.join(vulnurl))
        return vulnurl


    if output:
        save_it.save_func(final_uris , output , domain)
        print(f"\u001b[32m[+] Output is saved here :\u001b[31m \u001b[36moutput/{output}\u001b[31m" )
    else:
        print(f"\u001b[32m[+] Output not saved in any file.txt\u001b[31m")
    
    # return final_uris in json format
    return final_uris



def readFile(file):
    paths={
        "openredirect":"EndpointsParser/profiles/redirect.json",
        "xss":"EndpointsParser/profiles/xss.json",
        "xxe":"EndpointsParser/profiles/xxe.json",
        "sqli":"EndpointsParser/profiles/sqli.json",
        "sqlipost":"EndpointsParser/profiles/sqlipost.json",
    }
    with open(paths[file]) as json_file:
        data = json.loads(json_file.read())
        return data