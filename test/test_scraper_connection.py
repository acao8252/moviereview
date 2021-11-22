import os
import requests

def test():
    listOfURLs = [
    'https://www.imdb.com/showtimes/location',
    'https://www.metacritic.com/browse/movies/release-date/theaters/date?ttype=1&view=detailed',
    'https://www.rottentomatoes.com/browse/in-theaters',
    'https://www.themoviedb.org/remote/panel?panel=popular_scroller&group=in-theatres&language=en-US'
    ]

    accessedEverything = True
    for URL in listOfURLs:
        try:
            html = requests.get(URL)
            if(type(html.text) == type('test')):
                accessedEverything = accessedEverything and True
            else:
                accessedEverything = accessedEverything and False
        except:
            accessedEverything = accessedEverything and False

    return accessedEverything
