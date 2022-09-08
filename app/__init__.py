#-*- coding: utf-8 -*-
from flask import Flask, request, jsonify
from flask_cors import CORS
import numpy as np
#import app.model as model

app = Flask(__name__)
CORS(app)

@app.route('/')
def index():
    return 'Hello World!'
"""
@app.route('/predict', methods=['POST'])
def predict():
    insertValues = request.get_json()
    x1 = insertValues['x1']
    input = np.array([[x1]])
    print(input)
    result = model.result()
    return jsonify({'return':str(result)})
"""   
