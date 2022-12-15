import re

class Matchers:

    def __init__(self,matchCondition=None,matchtype=None,part=None,key=None,regex=None,code=None,payloads=None,rbody=None,responseData=None):
        self.matchCondition=matchCondition
        self.matchtype=matchtype
        self.part=part
        self.key=key
        self.regex=regex
        self.code=code
        self.payloads=payloads
        self.rbody=rbody
        self.responseData=responseData
       # print(self.headerMatch())
        #print(self.statusCodeMatch())
        #print(self.headerMatch())
        #print(self.bodyMatch())
        # print(self.isVulnerablity())
        # pprint.pprint(self.forAPI())



    def regex_match(self,pattern: str, string: str) -> bool:
        """Check if a string matches a regular expression pattern.
        
        Arguments:
            pattern: A string containing a regular expression pattern.
            string: The string to match against the pattern.
        
        Returns:
            True if the string matches the pattern, False otherwise.
        """
        try:
            # Compile the regular expression pattern
            regex = re.compile(pattern, re.MULTILINE | re.IGNORECASE)
            
            # Use the finditer() method to find matches in the string
            matches = regex.finditer(string)
            
            # If the iterator contains any matches, return True
            return any(matches)
        except Exception as e:
            # If an error occurred, print the error message and return False
            print(e)
            return False


    def isStatus(self):
        for match in self.matchtype:
            if match == 'status':
                return True
            


    def isRegex(self):
        for match in self.matchtype:
            if match == 'regex':
                return True



    def isBody(self):
        for match in self.part:
            if match == 'body':
                return True


    def isHeader(self):
        for match in self.part:
            if match == 'header':
                return True



    def statusCodeMatch(self):
        if self.isStatus():
            for payload in self.payloads:
                for key in self.responseData[payload]:
                    if key == 'status':
                        for code in self.code:
                            for c in code:
                                if self.responseData[payload][key] == c:
                                    return True,{
                                        "payload":payload,
                                        "status":self.responseData[payload][key],
                                        "matchtype":"status",
                                        "part":"status",
                                    }

                        


    def headerMatch(self):
        if self.isHeader():
            for payload in self.payloads:
                for key in self.responseData[payload]:
                    if key == 'headers':
                        for k in self.key:
                            if k in self.responseData[payload][key]:
                                for r in self.regex:
                                  string=f'{k}:{self.responseData[payload][key][k]}'
                                  if self.regex_match(r, string):        
                                    return True,{
                                        "payload":payload,
                                        "status":self.responseData[payload]['status'],
                                        "matchtype":"regex",
                                        "part":"header",
                                    }
                         

    def bodyMatch(self):
        if self.isBody():
            for payload in self.payloads:
                for key in self.responseData[payload]:
                    if key == 'data':
                        for r in self.regex:
                            if self.regex_match(r, str(self.responseData[payload][key])):
                                return True,{
                                    "payload":payload,
                                    "status":self.responseData[payload]['status'],
                                    "matchtype":"regex",
                                    "part":"body",
                                }



    def isVulnerablity(self):
        conditions=[self.statusCodeMatch(),self.headerMatch(),self.bodyMatch()]
        conditions = [c for c in conditions if c is not None] # remove None values
        if self.matchCondition == "and":
            if all(conditions):
                return True
        elif self.matchCondition == "or":
            if any(conditions): 
                return True


    def forAPI(self):
        # print in red color
        print("\033[91m {}\033[00m" .format("[!]Vulnerablity Found"))
        # print vulnerability information
        json=[]
        _json={}
        if self.isVulnerablity():
            if self.statusCodeMatch():
                con,match=self.statusCodeMatch()
                json.append(match)
            if self.headerMatch():
                con,match=self.headerMatch()
                json.append(match)
            if self.bodyMatch():
                con,match=self.bodyMatch()
                json.append(match)
            _json['data']=json
            return _json 