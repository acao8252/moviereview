from datetime import datetime

import json

import requests
from bs4 import BeautifulSoup

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

movieTupleList = list()
for movie in infoList:
    #print(movie)
    scrapedTitle = movie['title']
    scrapedTMeterScore = movie['tomatoScore']

    movieTuple = (scrapedTitle,scrapedTMeterScore, dateTimeScraped)
    movieTupleList.append(movieTuple)

    #print(movieTuple)
print(str(len(movieTupleList)), "movies scraped.")

# now we just export to a json file:
with open(('rottenTomatoesScrape'+dateScraped+'.json'), 'w') as f:
    jsonScrapedMovieDataList = json.dump(movieTupleList, f)
    #print(jsonScrapedMovieDataList)
