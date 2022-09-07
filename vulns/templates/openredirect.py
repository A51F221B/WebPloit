# this is a blueprint or template for openredirect attacks
id='Open Redirect'

request={
    'path':'/',
    'method': 'GET',
    'redirects':False,
    'payloads':True,
    'headers':{
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:68.0) Gecko/20100101 Firefox/68.0',
      
    },
}

matches=2
stopAtMatch=True


matcher0={
    'type':'regex',
    'part':'header',
    'name':'Location',
    'regex':'(?m)^(?:Location\s*?:\s*?)(?:https?:\/\/|\/\/|\/\\\\|\/\\)?(?:[a-zA-Z0-9\-_\.@]*)interact\.sh\/?(\/|[^.].*)?$'
}

matcher1={
    'type':'status',
    'status':[301,302,303,307,308],
    'condition':'or'
}


# payloads=['%0a/interact.sh/','%0d/interact.sh/','%00/interact.sh/','%09/interact.sh/',
#          '%5C%5Cinteract.sh/%252e%252e%252f']

#payloads=['Pages/About/Contact_Us.aspx']
payloads=['/j/exp/ERYIVUAW3VAMTPY6WYTWZX/index.js']
