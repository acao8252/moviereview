import json
import time
from datetime import datetime
from utils.imdb_api import imdb_api
from utils.youtube_api import get_trailer
from importlib import import_module
import sys

def manage(args):
    now = datetime.now()
    humanTime = now.strftime("%Y-%m-%d %H:%M")
    unixTime = round(time.time())

    massiveDataDict = {'humanTime':humanTime, 'unixTime':unixTime, 'movies':[]}

    listOfMovieDicts = []

    # one also needs to list the scrapers here:
    scrapersList = [
            "rottenTomatoes",
            "imdb",
            "tmdb",
            ]

    # NOTE: probably don't need id since react frontend can just list order by score
    id = 0

    if(len(args)==0):
        thingsToScrape = scrapersList # if not specified, scrape all scrapers.
    else:
        thingsToScrape = list()
        for arg in args:
            if (arg in scrapersList):
                thingsToScrape.append(arg)

    print("Scraping from", str(thingsToScrape),'\n')
    for scraper in thingsToScrape:
        # e.g. import scrapers.rottenTomatoesScraper
        movieList = import_module(f"scrapers.{scraper}").scrape()[0:10]

        for movie in movieList:

            rawTitle = movie["title"] # for searching via the imdb api.
            score = movie["score"]
            if(not score):
                score = 0

            votes = movie["votes"]

            imdb_dict = imdb_api(rawTitle)
            imdb_id = imdb_dict.get("tid")
            title = imdb_dict.get("title")
            poster = imdb_dict.get("poster")
            rating = imdb_dict.get("rating")
            director = imdb_dict.get("director")
            cast = imdb_dict.get("cast")
            plot = imdb_dict.get("plot")
            release = imdb_dict.get("release")
            genre = imdb_dict.get("genre")
            runtime = imdb_dict.get("runtime")

            scraperDict = {'name': scraper, 'score': score, 'votes': votes}
            print(scraperDict)

            # now we need to determine if the movie we just scraped is already
            # in the data structure or not.
            all_movie_values = [value for elem in massiveDataDict['movies'] for value in elem.values()]
            if(imdb_id in all_movie_values):

                # now that we know the movie is already stored just a matter
                # of getting that particular dictionary
                for alreadyStoredMovie in massiveDataDict['movies']:
                    if(alreadyStoredMovie['tid'] == imdb_id):
                        break

                # and add scraperDict to the list of scraperDicts:
                alreadyStoredMovie['scrapers'].append(scraperDict)

                # we're gonna take a different approach now to recompute score
                # a few basic necessities:
                # we want score to be an average weighted by number of users
                # however, we don't want any one source to dominate;
                # for instance, IMDB's massive userbase will skew any
                # resulting score in IMDB's favor, so our score would basically
                # just be IMDB's opinion of the movie.
                # therefore, we will also compute the flat average of
                # each website's score.
                # we will then average this average with the weighted average.
                # we call this the "triple average" system

                # first, the weighted average:
                tempScore1 = 0.0
                tempTotalVotes = 0
                scrapersWeight = len(scrapersList)
                for s in alreadyStoredMovie['scrapers']:
                    tmpVotes = s['votes']
                    tmpScore = s['score']
                    tempScore1+=float(tmpVotes * tmpScore)
                    tempTotalVotes += tmpVotes
                    scrapersWeight -= 1
                tempScore1 = tempScore1/float(tempTotalVotes)
                tempScore1 = tempScore1 - (tempScore1 / len(scrapersList) * scrapersWeight)

                # next, the straight average:
                tempScore2 = 0.0
                for s in alreadyStoredMovie['scrapers']:
                    tmpScore = s['score']
                    tempScore2 += float(tmpScore)
                tempScore2 = tempScore2/float(len(alreadyStoredMovie['scrapers']))
                tempScore2 = tempScore2 - (tempScore2 / len(scrapersList) * scrapersWeight)

                # and store it in our data struct.
                alreadyStoredMovie['score'] = round(((tempScore1 + tempScore2) / 2), 2)

            # if we didn't find an instance of the movie in the data object:
            else:
                # we need to find a link to the youtube:
                trailer = get_trailer(title)

                # also need to give weighted score for movies with only one scraper
                score = round(score/len(scrapersList), 2)

                # then we need to add a new movie to the data object:
                movieDict = {
                        'tid':imdb_id,
                        'title':title,
                        'poster':poster,
                        'rating':rating,
                        'score':score,
                        'director':director,
                        'cast':cast,
                        'plot':plot,
                        'release':release,
                        'genre':genre,
                        'runtime':runtime,
                        'trailer':trailer,
                        'scrapers':[scraperDict]
                        }
                massiveDataDict['movies'].append(movieDict)

    # sort the data by score so that the frontend won't have to
    massiveDataDict['movies'] = sorted(massiveDataDict['movies'], key=lambda m: m['score'], reverse=True)

    # now that we've done all that work constructing a massive dictionary,
    # we export the whole thing to a JSON file.
    # The JSON file will be named the current unix time.
    with open('json/'+str(unixTime)+'.json','w') as f:
        json.dump(massiveDataDict, f)

# if this is run as a script, we need this line to run the above funct
print("Usage: 'python manager.py [arguments]'")
print("If no arguments are supplied, then the manager will scrape using all known scrapers.")
print("If arguments ARE supplied, the manager will only scrape from arguments which match the scrapers' names.")
print("Example: 'python manager.py rottenTomatoes' will only scrape using the Rotten Tomatoes scraper.\n")
manage(sys.argv[1:])
