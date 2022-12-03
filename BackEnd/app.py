from flask import *
from flask_restful import Resource, Api
from Engine import scanner
from SubdomainScanner.subdomains import *
from flask import jsonify

'''
Create user input box

- User enters URL
- User specifies a specific endpoint

---

## In case of URL:


'''

app = Flask(__name__)
api = Api(app)

# defining all the general endpoints
@app.route('/')
def index():
    return render_template('templates/index.html')



# defining all the apis
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


