from datetime import datetime
from flask import Flask
from flask import render_template, redirect, url_for, abort
from utils.utils import ago
import json
import os

app = Flask(__name__)

# jinja filter
# convert unixtime to humantime for release date
@app.template_filter('conv_releasedate')
def conv_releasedate(unixtime):
     return datetime.fromtimestamp(unixtime).strftime('%b %d, %Y')

# convert unixtime to humantime for runtime
@app.template_filter('conv_runtime')
def conv_runtime(seconds):
    m, s = divmod(seconds, 60)
    h, m = divmod(m, 60)
    h = str(h)+'h'
    if m:
        m = f' {m}m'
    else:
        m = ""
    return f'{h}{m}'

@app.template_filter('conv_quotes')
def conv_quotes(string):
    string = string.replace("&apos;", "\'")
    string = string.replace("&quot;", "\"")
    return string

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
@app.route("/contact")
def contact():
    return render_template('contact.html')
