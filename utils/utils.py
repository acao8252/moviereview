import requests
import time
from bs4 import BeautifulSoup

def ago(unix_time):
    time_ago = time.time() - unix_time
    if(time_ago < 60):
        time_ago = int(time_ago)
        if(time_ago > 1):
            units = 'seconds'
        else:
            units = 'second'
    elif(time_ago >= 60 and time_ago < 3600):
        time_ago = time_ago / 60
        time_ago = int(time_ago)
        if(time_ago > 1):
            units = 'minutes'
        else:
            units = 'minute'
    elif(time_ago >= 3600 and time_ago < 86400):
        time_ago = time_ago / 60 / 60
        time_ago = int(time_ago)
        if(time_ago > 1):
            units = 'hours'
        else:
            units = 'hour'
    elif(time_ago >= 86400 and time_ago < 604800):
        time_ago = time_ago / 60 / 60 / 24
        time_ago = int(time_ago)
        if(time_ago > 1):
            units = 'days'
        else:
            units = 'day'
    else:
        time_ago = 'a'
        units = 'while'

    time_ago = f'{time_ago} {units} ago'
    return time_ago

def get_soup(url):
    headers = {'User-Agent': 'Mozilla/5.0 (Linux; Android 6.0.1; SHIELD Tablet K1 Build/MRA58K; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/55.0.2883.91 Safari/537.36'}

    html = requests.get(url, headers=headers).text
    soup = BeautifulSoup(html, 'html.parser')
    return soup
