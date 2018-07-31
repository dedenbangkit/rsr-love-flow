import json
import requests
from app.getflow import getFlow
from flask import Flask, jsonify
app = Flask(__name__)


URL = 'https://rsr.test.akvo.org/rest/v1/indicator_period_data_framework/?format=json&limit=1'
API_KEY = '7d9a17639015b614a8026868dcc0f90fe38a4268'

# Endpoints
# indicator_period_data_comment/?format=json
# indicator_period_data_framework/?format=json&limit=1
# post format in: app/post-format.py
# get flow data in: getflow.py


headers = {
    'content-type': 'application/json',
    'Authorization': 'Token {}'.format(API_KEY)
}

def post(data):
    r = requests.post(URL, data=json.dumps(data), headers=headers)
    status_code = r.status_code
    print(status_code)
    print(r.json())

@app.route('/')
def index():
    data = getFlow()
    return jsonify(data)

if __name__=='__main__':
    app.config.update(DEBUG=True, TEMPLATES_AUTO_RELOAD=True)
    app.run()
