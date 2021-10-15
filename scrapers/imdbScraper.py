import json
import requests
from bs4 import BeautifulSoup
from datetime import datetime

URL = "https://www.imdb.com/showtimes/location"

# maybe only need date rather than full datetime
date_within_json = datetime.now().strftime("%d/%m/%Y %H:%M")
date_title_json = datetime.now().strftime("%d-%m-%Y")

# TODO: should abstract this out into super class
html = requests.get(URL).text
soup = BeautifulSoup(html, "html.parser")
movie_list = soup.find_all("div", class_="lister-item")

# TODO: currently generating json lists; should instead be dictionary key-pairs
json_data = list()
for movie in movie_list:
    movie_data = list()
    title = movie.find("div", class_="title").text.strip()
    rating = movie.find(id="user_rating").find("strong").text.strip()

    # some movies may not have ratings; set to zero
    try:
        rating = float(rating) * 10
    except ValueError:
        rating = 0.0

    # convert from float to int and to str then append % to match rt scraper
    rating = str(int(rating)) + "%"

    # toss them all into a list
    movie_data.append(title)
    movie_data.append(rating)
    movie_data.append(date_within_json)

    # toss that into a superlist
    json_data.append(movie_data)

# TODO: temp code to generate json
with open(("imdbScrape" + date_title_json + ".json"), "w") as f:
    json.dump(json_data, f)
