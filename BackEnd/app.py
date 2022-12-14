import json
from SubdomainScanner.subdomains import Subdomains,Shodan
from flask import Flask, request, jsonify, Response, redirect, url_for


app = Flask(__name__)

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
            print(data['url'])
            subdomains = Shodan(data['url']).SearchDomains()
            print(subdomains)
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
