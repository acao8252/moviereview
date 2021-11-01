from flask import Flask
from flask import render_template
from utils.utils import ago
import json
import os

app = Flask(__name__)

@app.route("/")
def index():
    jsons = sorted(os.listdir('json'), reverse=True)[0:5]
    recent = json.load(open('json/' + jsons[0]))

    time_ago = ago(recent['unixTime'])
    return render_template('index.html', recent=recent, time_ago=time_ago)
