from utils.utils import get_soup
import os

def test():
    listOfURLs = [
    'https://www.imdb.com/showtimes/location',
    'https://www.metacritic.com/browse/movies/release-date/theaters/date?ttype=1&view=detailed',
    'https://www.rottentomatoes.com/browse/in-theaters',
    'https://www.themoviedb.org/remote/panel?panel=popular_scroller&group=in-theatres&language=en-US'
    ]

    accessedEverything = True
    for URL in listOfURLs:
        response = os.system("ping -c 1 " + URL)
        # reponse is zero if pinged, another number otherwise

        accessedEverything = accessedEverything and (not response)

    return accessedEverything
