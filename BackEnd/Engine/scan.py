import re
import json
import time
import sqlite3
from rich import print_json
from .components import req
from .components import matcher
from .components.reader import Reader


def setup_db():
    conn = sqlite3.connect("./Database/scan.db")
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS scan_count (total INTEGER)''')
    cursor.execute('''CREATE TABLE IF NOT EXISTS scan_durations (scan_id INTEGER PRIMARY KEY, duration REAL)''')
    conn.commit()
    cursor.execute("SELECT total FROM scan_count")
    if cursor.fetchone() is None:
        cursor.execute("INSERT INTO scan_count (total) VALUES (0)")
        conn.commit()
    conn.close()


def update_db_scan_count(count):
    conn = sqlite3.connect("./Database/scan.db")
    cursor = conn.cursor()
    cursor.execute("UPDATE scan_count SET total=?", (count,))
    conn.commit()
    conn.close()


def store_scan_duration(duration):
    conn = sqlite3.connect("./Database/scan.db")
    cursor = conn.cursor()
    cursor.execute("INSERT INTO scan_durations (duration) VALUES (?)", (duration,))
    conn.commit()
    conn.close()



class Scan:
    total_scan = 0

    def __init__(self, url, template):
        self.url = url
        self.template = template
        if not self.isValidUrl():
            print("Invalid URL")
            return

    @classmethod
    def increment_scan_count(cls):
        cls.total_scan += 1
        update_db_scan_count(cls.total_scan)

    @classmethod
    def get_total_scan(cls):
        return cls.total_scan

    @classmethod
    def initialize_scan_count(cls):
        conn = sqlite3.connect("./Database/scan.db")
        cursor = conn.cursor()
        cursor.execute("SELECT total FROM scan_count")
        result = cursor.fetchone()
        if result:
            cls.total_scan = result[0]
        conn.close()

    def main(self):
        start_time = time.time() # start time of the scan
        self.increment_scan_count()
        r=Reader(self.template)
        # reader is returning the request data and the req method is using those and returning response data
        self.headers, self.payloads, self.method, self.redirects = r.reader()
        self.rdata,self.rbody = req.Requester(self.url, self.template, self.headers, self.payloads, self.method, self.redirects).req()
        # reader will now return matchers from the template
        self.matchtype, self.part, self.key, self.regex,self.code,self.matchCondition,self.identity,self.info,self.severity = r.readMatchers()
        # after getting the response we will pass this response data to matcher class
        _json=matcher.Matchers(self.matchCondition,self.matchtype,self.part,self.key,self.regex,self.code,self.payloads,self.rbody,self.rdata,self.url,self.identity,self.info,self.severity).forAPI()
        end_time = time.time() # end time of the scan
        duration = end_time - start_time # total time taken for the scan
        store_scan_duration(duration) # store the duration in the database
        return json.dumps(_json, indent=4)
        

    def isValidUrl(self):
        regex = re.compile(
            r'^(?:http|ftp)s?://'  # http:// or https://
            r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+(?:[A-Z]{2,6}\.?|[A-Z0-9-]{2,}\.?)|'  # domain...
            r'localhost|'  # localhost...
            r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})'  # ...or ip
            r'(?::\d+)?'  # optional port
            r'(?:/?|[/?]\S+)$', re.IGNORECASE)
        
        return re.match(regex, self.url) is not None


Scan.initialize_scan_count()


#setup_db()

# Scan("https://0a38006c04e66ad4c4b8e2d500c600dc.web-security-academy.net/product/stock","blueprints/xxe.json")
#Scan("http://ptl-3983322e-008445f2.libcurl.so/redirect.php?uri=","blueprints/openredirect.json")

# Scan("https://0a9300b20367ec3dc10dbcbc005700b2.web-security-academy.net/product/stock","blueprints/xxe.json")