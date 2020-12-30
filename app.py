from flask import Flask, jsonify,request,make_response,url_for,redirect
from json import dumps
from requests import post
import pickle
from req import Parse
from analyze import FormRequestToModel
from sklearn.linear_model import Perceptron

nhash = 'analyze'

app = Flask(__name__)

@app.route("/"+str(nhash), methods=['GET', 'POST'])

def create_row_in_gs():
    if request.method == 'GET':
        return "Hello, Flask!"
    if request.method == 'POST':
        with open('model.pkl', 'rb') as f:
            model = pickle.load(f)
        url = request.json['url']
        content = Parse(url)
        if not content.isdigit():
            resp = (model.predict(FormRequestToModel(content)))
            return str(resp[0])
        return content