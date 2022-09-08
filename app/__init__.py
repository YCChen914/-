#-*- coding: utf-8 -*-
import os
from flask import Flask, request, render_template,jsonify
from flask_cors import CORS
import numpy as np
import app.model as model

#UPLOAD_FOLDER = './app/model'
ALLOWED_EXTENSIONS = set(['xlsx'])

app = Flask(__name__)
#app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
CORS(app)



@app.route('/test', methods=['GET'])
def test():
    return 'Hello World!'

@app.route('/upload',methods=['GET','POST'])
def upload():
    if request.method == 'GET':
        return render_template('index.html')
    else:
        file = request.files['file']
        if file:
            file.save(file.filename)
            num,feature,acc = model.result(file)
            return render_template('index.html',num=num,feature=feature,acc=acc)   