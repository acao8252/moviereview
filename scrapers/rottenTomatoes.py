import json
from utils.utils import get_soup

def scrape():
    URL = "https://www.rottentomatoes.com/browse/in-theaters"

    #page = requests.get(URL)
    #rottenTomatoSoup = BeautifulSoup(page.content, "html.parser")
    rottenTomatoSoup = get_soup(URL)

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
        scrapedScore = movie['tomatoScore']

        try:
            # in order to find the number of votes, we're going to have to access
            # each url given for the movie:
            scrapedURL = 'https://www.rottentomatoes.com' + movie['url']
            # this gives a working url
            movieSoup = get_soup(scrapedURL)
            #print(movieSoup.prettify())
            ratingsJson = movieSoup.find('script', id='score-details-json').text
            #print(ratingsJson)
            ratingsDict = json.loads(ratingsJson)
            #print(ratingsDict)

            # now we record the score and votes.
            # note that score has already been recorded.
            # Assuming nothing fails,
            # we'll just overwrite it here.
            scrapedScore = ratingsDict['scoreboard']['audienceScore']
            scrapedVotes = ratingsDict['scoreboard']['audienceCount']

            #print(str(scrapedVotes), "scraped votes for", scrapedTitle)
            #print(str(scrapedScore), "scraped score for", scrapedTitle)
        except Exception as e:
            # if there are any issues at all, let's set a default value of 1.
            scrapedVotes = 1

        # just to avoid divide by zero errors, we'll do this:
        if(scrapedVotes==0):
            scrapedVotes = 1

        #movieTuple = (scrapedTitle,scrapedScore, dateTimeScraped)
        movieData = {
            "title": scrapedTitle,
            "score": scrapedScore,
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

#if __name__ == "__main__":
#    from pprint import pprint
#    pprint(scrape())
