import requests
from bs4 import BeautifulSoup
from datetime import datetime

def scrape():
    url = "https://www.imdb.com/showtimes/location"

    # TODO: should abstract this out into super class
    html = requests.get(url).text
    soup = BeautifulSoup(html, "html.parser")
    raw_movie_list = soup.find_all("div", class_="lister-item")

    movie_list = list()
    for raw_movie in raw_movie_list:

        title = raw_movie.find("div", class_="title").text.strip()
        score = raw_movie.find(id="user_rating").find("strong").text.strip()

        # some movies may not have scores; set to zero
        try:
            score = round(float(score) * 10)
        except ValueError:
            score = 0

        # some movies may not have votes; set to zero
        try:
            votes = raw_movie.find("meta", {"itemprop":"ratingCount"})["content"]
        except TypeError:
            votes = 0

        movie_data = {
                "title": title,
                "score": score,
                "votes": votes,
                }

        # toss that into a superlist
        movie_list.append(movie_data)

    return movie_list

if __name__ == "__main__":
    from pprint import pprint
    pprint(scrape())
