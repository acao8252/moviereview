import json
import time
from datetime import datetime
from imdb_api import imdb_api
from importlib import import_module

def manage():
    now = datetime.now()
    humanTime = now.strftime("%Y-%m-%d %H:%M")
    unixTime = round(time.time())

    massiveDataDict = {'humanTime':humanTime, 'unixTime':unixTime, 'movies':[]}

    listOfMovieDicts = []

    # one also needs to list the scrapers here:
    scrapersList = [
            "imdb",
            "rottenTomatoes",
            "tmdb",
            ]

    # NOTE: probably don't need id since react frontend can just list order by score
    id = 0

    for scraper in scrapersList:
        movieList = import_module(f"{scraper}Scraper").scrape()

        # for right now, movieList consists of a list of tuples in the form:
        # (title,score,dateTimeScraped)
        # NOTE: probably better to have tuples as (title, score, votes)
        # since manager is already getting the date

        # I don't think that this formatting is perfect. I think we can
        # keep going anyway though.

        # only using top ten since, again, to avoid ip blocking from imdb
        for movie in movieList[0:10]:
            id+=1

            rawTitle = movie["title"] # for searching via the imdb api.
            score = movie["score"]


            # TODO: fix this section
            # these next items are all gonna be pulled using the imdb api,
            # in order to fix any issues with duplicates or inconsistent data.
            # I don't have the imdb api yet though, so it is TBD how this works

            imdb_dict = imdb_api(rawTitle)
            imdb_id = imdb_dict.get("tid")
            processedTitle = imdb_dict.get("title")
            poster = imdb_dict.get("poster")

            # will need to call another html page for each of their ratings
            # only requires O(n) to get the three items above
            # will require O(n^2) to just get the rating which could get us ip blocked
            #rating = imdb_api.search(movie.title).rating # encodes PG, R, etc

            # TODO: placeholder til all scrapers also pull votes
            votes = 0
            scraperDict = {'name': scraper, 'score': score, 'votes': votes}

            # now we need to determine if the movie we just scraped is already
            # in the data structure or not.
            all_movie_values = [value for elem in massiveDataDict['movies'] for value in elem.values()]
            if(imdb_id in all_movie_values):

                # now that we know the movie is already stored just a matter
                # of getting that particular dictionary
                for alreadyStoredMovie in massiveDataDict['movies']:
                    if(alreadyStoredMovie['tid'] == imdb_id):
                        break

                # recompute average score. This is ugly.
                # It averages the score over the current number of scrapers
                # in the scrapers list.
                alreadyStoredMovie['score'] = ((alreadyStoredMovie['score']*len(alreadyStoredMovie['scrapers'])) + score) / (1+len(alreadyStoredMovie['scrapers']))

                # and add scraperDict to the list of scraperDicts:
                alreadyStoredMovie['scrapers'].append(scraperDict)

                # finally, break:
                continue

            # if we didn't find an instance of the movie in the data object:
            else:
                # then we need to add a new movie to the data object:
                movieDict = {
                        #'id':id,
                        'tid':imdb_id,
                        'title':processedTitle,
                        #'rating':rating,
                        'score':score,
                        'poster':poster,
                        #'trailer':trailer,
                        'scrapers':[scraperDict]
                        }
                massiveDataDict['movies'].append(movieDict)

    # sort the data by score so that the frontend won't have to
    massiveDataDict['movies'] = sorted(massiveDataDict['movies'], key=lambda m: m['score'], reverse=True)

    # now that we've done all that work constructing a massive dictionary,
    # we export the whole thing to a JSON file.
    # The JSON file will be named the current unix time.
    with open(('json/'+str(unixTime)+'.json'),'w') as f:
        json.dump(massiveDataDict, f)

# if this is run as a script, we need this line to run the above funct
manage()
