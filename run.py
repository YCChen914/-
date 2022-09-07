from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

@app.route('/test')
def index():
    return 'Hello World!'
    
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)    