#-*- coding: utf-8 -*-
from fileinput import filename
import os
from flask import Flask, request, render_template,redirect,url_for
from flask_cors import CORS
import app.model as model
from werkzeug.utils import secure_filename

UPLOAD_FOLDER = './app/data'
ALLOWED_EXTENSIONS = set(['xlsx'])

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
CORS(app)



@app.route('/result/<filename>', methods=['GET'])
def result(filename):

    ans1 ,ans2,ans3  = model.result(filename)
    return render_template('index.html',num = ans1,feature = ans2,acc = ans3)#render_template('index.html')

@app.route('/upload',methods=['GET','POST'])
def upload():
    if request.method == 'GET':
        return render_template('index.html')
    else:
        file = request.files['file']
        if file:
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            return redirect(url_for('result',filename=filename))

         

