from flask import Flask
from flask import render_template, redirect, url_for, abort
from utils.utils import ago
import json
import os

app = Flask(__name__)

@app.route("/")
@app.route("/<int:page>")
def index(page=0):
    jsons = sorted(os.listdir('json'), reverse=True)

    if page and page > 0:
        index = page
    else:
        index = 0

    try:
        recent = json.load(open('json/' + jsons[index]))
    except IndexError:
        abort(404)

    time_ago = ago(recent['unixTime'])
    return render_template('index.html', recent=recent, page=page, time_ago=time_ago)
