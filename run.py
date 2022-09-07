from flask import Flask, request, jsonify
from flask_cors import CORS
import numpy as np

app = Flask(__name__)
CORS(app)

@app.route('/')
def index():
    return 'Hello World!'

@app.route('/predict', methods=['POST'])
def predict():
    insertValues = request.get_json()
    x1 = insertValues['x1']
    input = np.array([[x1]])
    print(input)
    return jsonify({'return':'ok'})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)    