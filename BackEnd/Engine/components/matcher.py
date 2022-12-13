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
        # print(self.statusCodeMatch())
        #print(self.headerMatch())
        #print(self.bodyMatch())
        print(self.isVulnerablity())


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
                                    return True

                        


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
                                     return True
                         

    def bodyMatch(self):
        if self.isBody():
            for payload in self.payloads:
                for key in self.responseData[payload]:
                    if key == 'data':
                        for r in self.regex:
                            if self.regex_match(r, str(self.responseData[payload][key])):
                                return True



    def isVulnerablity(self):
        conditions=[self.statusCodeMatch(),self.headerMatch(),self.bodyMatch()]
        conditions = map(lambda x: x if x is not None else False, conditions)
        if self.matchCondition == "and":
            if all(conditions):
                return True
        elif self.matchCondition == "or":
            if any(conditions): 
                return True
        

