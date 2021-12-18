from flask import Flask, request, json
from flask_cors import CORS

app = Flask(__name__)


@app.route('/testing', methods=['GET', 'POST'])
def sample():
    return "tested"