from flask import Flask, jsonify, request, make_response, url_for, redirect
from json import dumps
from requests import post
import pickle
from req import parse
from preparation import form_query_to_model
from sklearn.linear_model import Perceptron
import pandas as pd

nhash = 'analyze'

app = Flask(__name__)

@app.route("/" + nhash, methods=['GET', 'POST'])

def create_row_in_gs():
    if request.method == 'GET':
        return "Hello, Stranger!"
    if request.method == 'POST':
        df_trained = pd.read_csv('train_server.csv')
        url = request.json['url']
        content = parse(url)
        if not content.isdigit():
            resp = (model.predict(form_query_to_model(url, content)))
            return str(resp[0])
        return get_error_encode(content)