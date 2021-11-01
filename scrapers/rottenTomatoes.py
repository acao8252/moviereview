from datetime import datetime

import json

import requests
from bs4 import BeautifulSoup

def scrape():
    URL = "https://www.rottentomatoes.com/browse/in-theaters"

    now = datetime.now()
    dateTimeScraped = now.strftime("%d/%m/%Y %H:%M")
    dateScraped = now.strftime("%d-%m-%Y")
    page = requests.get(URL)
    rottenTomatoSoup = BeautifulSoup(page.content, "html.parser")

    scripts = rottenTomatoSoup.find_all("script")

    # lord forgive me this hardcoding:
    #print(scripts[39].prettify())

    scriptWithInfo = scripts[39].text
    #print(scriptWithInfo)
    for i in range(len(scriptWithInfo)):
        if(scriptWithInfo[i:i+6] == '[{"id"'):
            strippedString=scriptWithInfo[i:]
            break
    #print(strippedString)
    for i in range(len(strippedString)):
        if(strippedString[i:i+3]=='}],'):
            strippedString=strippedString[:i+2]
            break
    #print(strippedString)
    infoList = json.loads(strippedString)
    #print(infoList)

    movieDataList = list()
    for movie in infoList:
        #print(movie)
        scrapedTitle = movie['title']
        scrapedTMeterScore = movie['tomatoScore']
        scrapedVotes = 1 # I can't pull this from rottenTomatoes!
        # setting this number to 1 so that don't have "divide by zero" errors

        #movieTuple = (scrapedTitle,scrapedTMeterScore, dateTimeScraped)
        movieData = {
            "title": scrapedTitle,
            "score": scrapedTMeterScore,
            "votes": scrapedVotes,
        }
        movieDataList.append(movieData)

        #print(movieTuple)
    print(str(len(movieDataList)), "movies scraped.")

    # now we just export to a json file:
    #with open(('rottenTomatoesScrape'+dateScraped+'.json'), 'w') as f:
        #jsonScrapedMovieDataList = json.dump(movieTupleList, f)
        #print(jsonScrapedMovieDataList)
    return movieDataList

if __name__ == "__main__":
    from pprint import pprint
    pprint(scrape())
