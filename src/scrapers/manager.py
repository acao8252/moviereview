from datetime import datetime
import json

# the scrapers need to be listed here:
from rottenTomatoesScraper import scrape
from imdbScraper import scrape

def manage():
    now = datetime.now()
    humanTime = now.strftime("%d-%m-%Y %H:%M")
    unixTime = now.fromtimestamp()

    massiveDataDict = {'humanTime':humanTime, 'unixTime':unixTime, 'movies':[]}

    listOfMovieDicts = []

    # one also needs to list the scrapers here:
    scrapersList = [imdbScraper, rottenTomatoesScraper]

    id = 0

    for scraper in scrapersList:
        movieList = scraper.scrape()

        # for right now, mvoieList consists of a list of tuples in the form:
        # (title,score,dateTimeScraped)

        # I don't think that this formatting is perfect. I think we can
        # keep going anyway though.

        for movie in movieList:
            id+=1

            rawTitle = movie[0] # for searching via the imdb api.
            score = movie[1]


            # TODO: fix this section
            # these next items are all gonna be pulled using the imdb api,
            # in order to fix any issues with duplicates or inconsistent data.
            # I don't have the imdb api yet though, so it is TBD how this works

            #imdb_id = imdb_api.search(movie.title.id).id
            #processedTitle = imdb_api.search(rawTitle).title
            #poster = imdb_api.search(movie.title).poster
            #rating = imdb_api.search(movie.title).rating # encodes PG, R, etc

            scraperDict = {'name':str(scraper), 'score': score, 'votes': votes}

            # now we need to determine if the movie we just scraped is already
            # in the data structure or not.
            for alreadyStoredMovie in massiveDataDict['movies']:
                matched=(alreadyStoredMovie['tid']==imdb_id)

                if matched:
                    # recompute average score. This is ugly.
                    # It averages the score over the current number of scrapers
                    # in the scrapers list.
                    alreadyStoredMovie['score'] = ((alreadyStoredMovie['score']*len(alreadyStoredMovie['scrapers'])) + score) / (1+len(alreadyStoredMovie['scrapers']))

                    # and add scraperDict to the list of scraperDicts:
                    alreadyStoredMovie['scrapers'].append(scraperDict)

                    # finally, break:
                    break

            # if we didn't find an instance of the movie in the data object:
            if not matched:
                # then we need to add a new movie to the data object:
                movieDict = {'id':id,'tid':imdb_id,'title':processedTitle,'rating':rating,'score':score,'poster':poster,'trailer':trailer,'scrapers':[scraperDict]}
                massiveDataDict['movies'].append(movieDict)

    # now that we've done all that work constructing a massive dictionary,
    # we export the whole thing to a JSON file.
    # The JSON file will be named the current unix time.
    with open((str(unixTime)+'.json'),'w') as f:
        json.dump(massiveDataDict, f)

manage() # if this is run as a script, we need this line to run the above funct
