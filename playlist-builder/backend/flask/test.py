from flask import Flask, request, json
from flask_cors import CORS
import json

app = Flask(__name__)

data = []


@app.route('/getData', methods=['POST'])
def dataFromUser():
    data = request.get_data(as_text=True)
    d = json.loads(data)
    print(d["songName"])
    return data