import imdb
import re
import requests
from bs4 import BeautifulSoup

def imdb_api(query):
    data = {
            "id": None,
            "title": None,
            "poster": None,
            "rating": None,
            }
    url = f"https://www.imdb.com/find?q={query}&s=tt&ttype=ft&ref_=fn_ft"
    html = requests.get(url).text
    soup = BeautifulSoup(html, "html.parser")

    ia = imdb.IMDb()
    search_table = soup.find("table", class_="findList")

    # return first movie on list
    title = search_table.find("td", class_="result_text").find("a").text.strip()

    # anchor with nested poster image
    anchor = search_table.find("td", class_="primary_photo").find("a", href=True)
    # get tid from anchor url
    movie_url = anchor["href"]
    tid = re.search("\/title\/(tt\d+)\/", movie_url).group(1)

    # url manipulation to get full-sized poster image
    tiny_poster = anchor.find("img")["src"]
    poster = re.sub("\_.*\_\.", "", tiny_poster)

    data["id"] = tid
    data["title"] = title
    data["poster"] = poster

    return data

if __name__ == "__main__":
    from pprint import pprint
    query = "not time to die"
    data = imdb_api(query)
    pprint(data)
