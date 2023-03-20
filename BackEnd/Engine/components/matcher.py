
import re
from typing import Tuple, Union


class Matchers:
    def __init__(self, match_condition=None, match_type=None, part=None, key=None, regex=None, code=None, payloads=None,
                 r_body=None, response_data=None,url=None):
        self.match_condition = match_condition
        self.match_type = match_type or []
        self.part = part or []
        self.key = key or []
        self.regex = regex or []
        self.code = code or []
        self.payloads = payloads or []
        self.r_body = r_body
        self.response_data = response_data or {}
        self.url=url

    def regex_match(self, pattern: str, string: str) -> bool:
        try:
            regex = re.compile(pattern, re.MULTILINE | re.IGNORECASE)
            return any(regex.finditer(string))
        except re.error:
            return False

    def isStatus(self) -> bool:
        return 'status' in self.match_type

    def isRegex(self) -> bool:
        return 'regex' in self.match_type

    def isBody(self) -> bool:
        return 'body' in self.part

    def isHeader(self) -> bool:
        return 'header' in self.part

    def statusCodeMatch(self) -> Union[None, Tuple[bool, dict]]:
        if not self.isStatus():
            return None

        for payload in self.payloads:
            response = self.response_data.get(payload)
            if not response:
                continue

            status = response.get('status')
            if not status:
                continue

            for codes in self.code:
                if str(status) in codes:
                    return True, {
                        "payload": payload,
                        "status": status,
                        "matchtype": "status",
                        "part": "status",
                    }


    def headerMatch(self) -> Union[None, Tuple[bool, dict]]:
        if not self.isHeader():
            return None

        for payload in self.payloads:
            response = self.response_data.get(payload)
            if not response:
                continue

            headers = response.get('headers')
            if not headers:
                continue

            for key in self.key:
                header_value = headers.get(key)
                if not header_value:
                    continue

                for r in self.regex:
                    string = f'{key}:{header_value}'
                    if self.regex_match(r, string):
                        return True, {
                            "payload": payload,
                            "status": response['status'],
                            "matchtype": "regex",
                            "part": "header",
                        }

    def bodyMatch(self) -> Union[None, Tuple[bool, dict]]:
        if not self.isBody():
            return None

        for payload in self.payloads:
            response = self.response_data.get(payload)
            if not response:
                continue

            data = response.get('data')
            if not data:
                continue

            for r in self.regex:
                if self.regex_match(r, str(data)):
                    return True, {
                        "payload": payload,
                        "status": response['status'],
                        "matchtype": "regex",
                        "part": "body",
                    }

    def isVulnerablity(self) -> bool:
        conditions = [self.statusCodeMatch(), self.headerMatch(), self.bodyMatch()]
        conditions = [c for c in conditions if c is not None]  # remove None values
        if self.match_condition == "and":
            return all(conditions)
        elif self.match_condition == "or":
            return any(conditions)
        else:
            return False


    def forAPI(self) -> dict:
        if not self.isVulnerablity():
            return {"data": "No Vulnerability Found"}

        print("\033[91m {}\033[00m".format("[!] Vulnerability Found"))

        json_data = []
        statusCodeMatch = self.statusCodeMatch()
        headerMatch = self.headerMatch()
        bodyMatch = self.bodyMatch()

        if statusCodeMatch:
            json_data.append(statusCodeMatch[1])
        if headerMatch:
            json_data.append(headerMatch[1])
        if bodyMatch:
            json_data.append(bodyMatch[1])
        json_data.append({"url":self.url})
        return {"data": json_data}

