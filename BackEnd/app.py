import json
import sqlite3
from Engine.scan import Scan
from EndpointsParser.parser import init
from SubdomainScanner.subdomains import Subdomains
from flask import Flask, request, jsonify, Response, redirect, url_for
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from auth import db, User

import logging

app = Flask(__name__)
app.config['SECRET_KEY'] = 'mysecretkey'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////Users/macvision/Documents/Webploit/BackEnd/Database/users.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize Flask-Login
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'signin'

db.init_app(app)

# Configuring logging
logging.basicConfig(filename='server.log', level=logging.INFO)
file_handler = logging.FileHandler('server.log')
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
file_handler.setFormatter(formatter)
app.logger.addHandler(file_handler)

# Configuring database
DATABASE = 'Database/api.db'

def get_db():
    conn = sqlite3.connect(DATABASE)  # connect to database
    conn.row_factory = sqlite3.Row
    return conn



from flask import current_app

@app.before_first_request
def setup_db():
    with app.app_context():
        db.create_all()


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@app.route('/signin', methods=['POST'])
def signin():
    data = request.get_json()
    user = User.query.filter_by(email=data['email']).first()

    if user and user.check_password(data['password']):
        login_user(user)
        return jsonify({"status": "success", "message": "Logged in successfully"}), 200
    else:
        return jsonify({"status": "error", "message": "Invalid email or password"}), 401

@app.route('/signup', methods=['POST'])
def signup():
    data = request.get_json()
    email = data['email']
    password = data['password']

    user = User.query.filter_by(email=email).first()
    if user:
        return jsonify({"status": "error", "message": "Email already exists"}), 409

    new_user = User(email=email)
    new_user.set_password(password)

    db.session.add(new_user)
    db.session.commit()

    return jsonify({"status": "success", "message": "User created successfully"}), 201


HTTP_METHODS = ['GET', 'HEAD', 'POST', 'PUT', 'DELETE', 'CONNECT', 'OPTIONS', 'TRACE', 'PATCH']

@app.route('/', methods=HTTP_METHODS)
def index():
    return redirect(url_for('base'))

@app.route('/base', methods=HTTP_METHODS)
def base():
    with open('version.conf') as f:
        version = f.read()
    return {
        "Server": "WebPloit API server",
        "Version": version
    }



@app.route('/api/subdomains', methods=['POST','GET'])
def subdomains():
    if request.method == 'POST':
        try:
            content_type=request.headers.get('Content-Type')
            if content_type == 'application/json':
                data=request.json
            else:
                data=request.form.to_dict() 
            if data==None or data=={}:
                return {
                    "status": "error",
                    "message": "No data provided"
                },500
            
            if not data.get('url'):
                return {
                    "status": "error",
                    "message": "No url provided"
                },500
            elif not data.get('aggressive'):
                aggressive=False
            elif data.get('aggressive')=='true':
                aggressive=True
            elif data['url']=="": 
                return {
                    "status": "error",
                    "message": "No url provided"
                },500
            # try:
            #     subdomains = Shodan(data['url']).SearchDomains()
            # except:
            subdomains = Subdomains(data["url"]).forAPI()
            return {
                "status": "success",
                "message": "Subdomains found",
                "data": subdomains
            },200
        except Exception as E:
            return {
                "status" : "error",
                "Details" : f'Invalid Request. Error: {E}'
            }, 500
    elif request.method == 'GET':
        with open('Found_Subdomains.json') as f:
            data = json.load(f)
        return {
            "status": "success",
            "message": "Subdomains found",
            "data": data
        },200



@app.route('/api/endpoints', methods=['POST'])
def endpoints():
    try:
        content_type=request.headers.get('Content-Type')
        if content_type == 'application/json':
            data=request.json
        else:
            data=request.form.to_dict()
        # check if any of the parameters are missing or none
        if data==None or data=={}:
            return {
                "status": "error",
                "message": "No data provided"
            },500
        if not data.get('url') or data['url']=="":
            return {
                "status": "error",
                "message": "No url provided"
            },500
        # defining the default values for optional parameters
        values={
            'subs':True,
            'level':None,
            'exclude':None,
            'output':None,
            'placeholder':"",
            'quiet':None,
            'retries':3,
            'vulns':None
        }
        # parse optional parameters like subs=None,level=None,exclude=None,output=None,placeholder=None,quiet=None,retries=None,vulns=None
        if data.get('subs') and data['subs']=='false':
            # update the value of subs in values
            values['subs']=data['subs']
        if data.get('level'):
            values['level']=data['level']
        if data.get('exclude'):
            values['exclude']=data['exclude']
        if data.get('output'):
            values['output']=data['output']
        if data.get('placeholder'):
            values['placeholder']=data['placeholder']
        if data.get('quiet'):   
            values['quiet']=data['quiet']
        # making sure user doesn't enter a negative value for retries or a value greater than 5
        if data.get('retries') and int(data['retries'])>0 and int(data['retries'])<=5:
            values['retries']=data['retries']

        # making sure that vulns if from ['openredirect','xss','sqli','xxe']
        if data.get('vulns') and data['vulns'] in ['openredirect','xss','sqli','xxe']:
            values['vulns']=data['vulns']
        else:
            return {
                "status": "error",
                "message": "Invalid value for vulns"
            },500
        # calling the init function from parser.py
        data=init(
            data['url'],
            subs=values['subs'],
            level=values['level'],
            exclude=values['exclude'],
            output=values['output'],
            placeholder=values['placeholder'],
            quiet=values['quiet'],
            retries=values['retries'],
            vulns=values['vulns']
        )
        return {
            "status": "success",
            "message": "Endpoints found",
            "data": data
        },200
    except Exception as E:
        return {
            "status" : "error",
            "Details" : f'Invalid Request. Error: {E}'
        }, 500
    
     


@app.route('/api/scan', methods=['POST'])
def scan():
    content_type = request.headers.get('Content-Type')
    if content_type == 'application/json':
        data = request.json
    else:
        data = request.form.to_dict()
    if data is None or data == {}:
        return {
            "status": "error",
            "message": "No data provided"
        }, 500
    if not data.get('url') or data['url'] == "":
        return {
            "status": "error",
            "message": "No url provided"
        }, 500
    if not data.get('vuln') or data['vuln'] == "":
        return {
            "status": "error",
            "message": "No vulnerability specified"
        }, 500
    if data['vuln'] not in ['openredirect','xxe','sqli']:
        return {
            "status": "error",
            "message": "Invalid vulnerability specified"
        }, 500

    path = {
        'openredirect': 'Engine/blueprints/openredirect.json',
        'xxe': 'Engine/blueprints/xxe.json',
        "sqli": "Engine/blueprints/sqli.json"
    }
    res = Scan(data['url'], path[data['vuln']]).main()
    print(res)

    # Parse the JSON string returned by the main function
    res_data = json.loads(res)

    return {
        "status": "success",
        "message": "Scan completed",
        "data": res_data
    }, 200
