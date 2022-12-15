import json
from Engine.scan import Scan
from EndpointsParser.parser import init
from SubdomainScanner.subdomains import Subdomains,Shodan
from flask import Flask, request, jsonify, Response, redirect, url_for

import logging
__log__=logging.getLogger('werkzeug')  
__log__.setLevel(logging.ERROR) # will record only errors

file_handler = logging.FileHandler('server.log')

app = Flask(__name__)
app.logger.addHandler(file_handler)

HTTP_METHODS = ['GET', 'HEAD', 'POST', 'PUT', 'DELETE', 'CONNECT', 'OPTIONS', 'TRACE', 'PATCH']

@app.route('/', methods=HTTP_METHODS)
def index():
    return redirect(url_for('base'))

@app.route('/base',methods=HTTP_METHODS)
def base():
    with open('version.conf') as f:
        version = f.read()
    return {
        "Server":"WebPloit API server",
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
            subdomains = Subdomains(data['url'],aggressive).toJson()
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
    if not data.get('url') or data['url']=="":
        return {
            "status": "error",
            "message": "No url provided"
        },500
    if not data.get('vuln') or data['vuln']=="":
        return {
            "status": "error",
            "message": "No vulnerability specified"
        },500
    if data['vuln'] not in ['openredirect','xxe']:
        return {
            "status": "error",
            "message": "Invalid vulnerability specified"
        },500

    path={
        'openredirect':'Engine/blueprints/openredirect.json',
        'xxe':'Engine/blueprints/xxe.json'
    }
    res=Scan(data['url'],path[data['vuln']]).main()
    print(res)
    return {
        "status": "success",
        "message": "Scan completed",
        "data": res
    },200
    