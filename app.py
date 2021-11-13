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
    colors = [
            '220,53,69', #red
            '255,193,7', #yellow
            '25,135,84', #green
            '13,110,253', #blue
            '102,16,242', #indigo
            ]

    jsons = sorted(os.listdir('json'), reverse=True)

    if page and page > 0:
        index = page
    else:
        index = 0

    try:
        recent = json.load(open('json/' + jsons[index]))
    except IndexError:
        abort(404)

    top_five = recent.get('movies')[0:5]

    graph_y = list()
    graph_x = list()
    color_count = 0
    for movie in top_five:
        top_movie = {
                'title': movie.get('title'),
                }
        if(recent.get('unixTime') not in graph_y):
            graph_y.append(recent.get('unixTime'))
        scores = list()
        scores.append(movie.get('score'))
        count = 1
        while(count < 5):
            try:
                next_recent = json.load(open('json/' + jsons[index+count]))
                next_movies = next_recent.get('movies')
                for next_movie in next_movies:
                    if(next_recent.get('unixTime') not in graph_y):
                        graph_y.append(next_recent.get('unixTime'))
                    if(next_movie.get('tid') == movie.get('tid')):
                        scores.append(next_movie.get('score'))
                        break
            except IndexError:
                break
            count += 1
        graph_x.append({
            'title': movie.get('title'),
            'scores': scores,
            'color': colors[color_count]
            })
        color_count += 1


    time_ago = ago(recent['unixTime'])
    return render_template('index.html', recent=recent, graph_y=graph_y, graph_x=graph_x, page=page, time_ago=time_ago)

@app.route("/contact")
def contact():
    return render_template('contact.html')
