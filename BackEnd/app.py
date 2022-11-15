from flask import *
from flask_restful import Resource, Api
from Engine import scanner
from SubdomainScanner.subdomains import *


'''
Create user input box

- User enters URL
- User specifies a specific endpoint

---

## In case of URL:


'''

app = Flask(__name__)
api = Api(app)


# @app.route("/")
# def home():
#     # Render a template
#     return render_template("index.html")


# def parser(attack_type):
#     # url = request.args.get('url')
#     # print(url)
#     url = request.form.get('text')
#     # Test case to check if the url is valid
#     ''' HERE '''
#     #x = scanner.start(url = url, attack_type=attack_type)
#     x = Subdomains(url, False).GetSubdomains()
#     print(x)
#     return render_template_string(x)


# def readSubdomains():
#     with open("./Found_Subdomains.json") as f:
#         data = json.loads(f.read())
#         return data



# @app.route("/api/subdomains", methods=['GET'])
# def subdomains():
#     # display json data on this endpoint
#     return readSubdomains()



# @app.route("/api/xxe", methods=["POST"])
# def xxe():
#     return parser("xxe")

# # @app.route("/api/open_redirect", methods=["POST"])
# # def open_direct():
# #     return parser("open_redirect")


# @app.route("/api/subdomains", methods=["POST"])
# def open_direct():
#     return parser("open_redirect")



class subdomains(Resource):
    def get(self):
        with open("./Found_Subdomains.json") as f:
            data = json.loads(f.read())
            return data

    def post(self):
        url = request.form.get('text')
        print(url)
        x = Subdomains(url, aggressive=False)
        print(x)
        #return render_template_string(x)




api.add_resource(subdomains, '/api/subdomains')


class XXE(Resource):
    def post(self):
        url = request.form.get('text')
        x = scanner.start(url = url, attack_type="xxe")
        print(x)
        return render_template_string(x)