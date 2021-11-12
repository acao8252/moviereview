import json
import re
import requests
from bs4 import BeautifulSoup
from datetime import datetime

def imdb_api(query):
    print(query)
    data = {
            "tid": None,
            "title": None,
            "poster": None,
            "rating": None,
            "director": None,
            "cast": None,
            "plot": None,
            "release": None,
            "genre": None,
            "runtime": None,
            }
    query = query.replace(" ", "+")
    url = f"https://www.imdb.com/find?q={query}&s=tt&ttype=ft&ref_=fn_ft"
    html = requests.get(url).text
    soup = BeautifulSoup(html, "html.parser")

    search_table = soup.find("table", class_="findList")

    # return first movie on list
    # this try-catch is here because "The Reluctant Convert" is a TV Movie
    # and the first url is only for theater movies
    try:
        title = search_table.find("td", class_="result_text").find("a").text.strip()
    except AttributeError:
        url = f"https://www.imdb.com/find?q={query}&ref_=nv_sr_sm"
        html = requests.get(url).text
        soup = BeautifulSoup(html, "html.parser")
        search_table = soup.find("table", class_="findList")
        title = search_table.find("td", class_="result_text").find("a").text.strip()

    # anchor with nested poster image
    anchor = search_table.find("td", class_="primary_photo").find("a", href=True)
    # get tid from anchor url
    movie_url = anchor["href"]
    tid = re.search("\/title\/(tt\d+)\/", movie_url).group(1)

    url = f"https://www.imdb.com/title/{tid}/"
    html = requests.get(url).text
    soup = BeautifulSoup(html, "html.parser")

    # find particular script tag with json elements
    script = soup.find("script", type="application/ld+json").text
    script = json.loads(script)

    plot = script.get("description")
    rating = script.get("contentRating")
    poster = script.get("image")
    genre = script.get("genre")

    try:
        director = script.get("director")[0].get("name")
    except TypeError:
        director = None
    actors = script.get("actor")
    cast = list()
    if actors:
        for actor in actors:
            cast.append(actor.get("name"))

    # make sure the unix time is a nice whole number
    release = script.get("datePublished")
    if release:
        release = datetime.strptime(release, "%Y-%m-%d").timestamp()
        release = round(release)

    # "duration" comes in the form of "PT1H37M"
    # convert that to 5820 seconds
    runtime = script.get("duration")
    if runtime:
        #TODO: need to rework this; maybe use a different script tag to get data
        try:
            match = re.search("PT(\d+)H(\d+)M", runtime)
            hour = int(match.group(1)) * 3600
            minute = int(match.group(2)) * 60
        except AttributeError:
            match = re.search("PT(\d+)H", runtime)
            hour = int(match.group(1)) * 3600
            minute = 0
        runtime = hour + minute

    data["tid"] = tid
    data["title"] = title
    data["poster"] = poster
    data["director"] = director
    data["cast"] = cast
    data["rating"] = rating
    data["plot"] = plot
    data["genre"] = genre
    data["release"] = release
    data["runtime"] = runtime

    return data

if __name__ == "__main__":
    from pprint import pprint
    query = "the most reluctant convert"
    query = "the last warning"
    query = "venom let there be carnage"
    query = "many saints of newark"
    data = imdb_api(query)
    pprint(data)
