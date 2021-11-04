#import imdb
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

    # url manipulation to get full-sized poster image
    tiny_poster = anchor.find("img")["src"]
    poster = re.sub("\_.*\_\.", "", tiny_poster)

    """
    # now use imdb api to get the rest
    ia = imdb.IMDb()

    # api does not like the tt prefix in id
    imdb_id = tid.replace("tt", "")
    mov = ia.get_movie(imdb_id)

    # get people
    director = mov.get('directors')[0].get('name')
    cast = list()
    for person in mov.get('cast')[0:5]:
        cast_name = person.get('name')

        # seems some just don't have roles
        try:
            cast_role = person.currentRole.get('name')
        except AttributeError:
            cast_role = None
            print(tid)
            print(title)
            print(cast_name)

        person_id = person.getID()
        cast_member = ia.get_person(person_id)

        # some just don't have headshots
        try:
            tiny_cast_image = cast_member.get('headshot')
            cast_image = re.sub("\_.*\_\.", "", tiny_cast_image)
        except TypeError:
            cast_image = None

        cast.append(
                {
                    'name': cast_name,
                    'role': cast_role,
                    'image': cast_image
                    }
                )

    # get rating e.g. PG-13
    certs = mov.get('certificates')
    rating = None
    for cert in certs:
        if(cert == "United States:G"):
            rating = "G"
            break
        elif(cert == "United States:PG"):
            rating = "PG"
            break
        elif(cert == "United States:PG-13"):
            rating = "PG-13"
            break
        elif(cert == "United States:R"):
            rating = "R"
            break

    # get the release date
    raw_date = mov.get('original air date')
    raw_date = raw_date.replace(" (USA)", "")
    release = datetime.strptime(raw_date, "%d %b %Y").timestamp()
    release = int(release)

    # get the plot
    plot = mov.get('plot outline')

    # get the genre
    genre = mov.get('genre')
    """

    data["tid"] = tid
    data["title"] = title
    data["poster"] = poster
    #data["director"] = director
    #data["cast"] = cast
    #data["rating"] = rating
    #data["plot"] = plot
    #data["genre"] = genre
    #data["release"] = release

    return data

if __name__ == "__main__":
    from pprint import pprint
    query = "venom let there be carnage"
    data = imdb_api(query)
    pprint(data)
