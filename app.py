from flask import Flask, request
import scanner

'''
Create user input box

- User enters URL
- User specifies a specific endpoint

---

## In case of URL:


'''

app = Flask(__name__)


@app.route("/")
def home():
    return "Test"


@app.route("/api/xss")
def xss():
    url = request.args.get('url')
    scanner.start(url=url)
    pass
