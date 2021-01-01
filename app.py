from flask import Flask, jsonify,request,make_response,url_for,redirect
from flask_cors import CORS
from json import dumps
from requests import post
import pickle
from req import Parse
from analyze import FormRequestToModel
from sklearn.linear_model import Perceptron

nhash = 'analyze'

app = Flask(__name__)
CORS(app)

@app.route("/")
def PrintHello():
    return "HELLO"

@app.route("/"+str(nhash), methods=['GET', 'POST'])

def process_request():
    if request.method == 'GET':
        return "Wrong type of request!"
    if request.method == 'POST':
        with open('model.pkl', 'rb') as f:
            model = pickle.load(f)
        url = request.json['url']
        content = Parse(url)
        if not content.isdigit():
            result = model.predict(FormRequestToModel(content))
            resp = make_response(str(result[0]))
            resp.headers['Access-Control-Allow-Origin']='*'
            return resp
        resp = make_response('205')
        resp.headers['Access-Control-Allow-Origin']='*'
        return resp