from youtubesearchpython import VideosSearch

def get_trailer(movieName):
    # given a movie's name (as a string!) we can find the trailer, hopefully.

    '''modifiedMovieNameForURL = ""
    for char in movieName:
        if (char==' '):
            modifiedMovieNameForURL += '+'
        else:
            modifiedMovieNameForURL += char.lower()

    # now modifiedMovieNameForURL is in the format we need, construct URL
    URL='https://www.youtube.com/results?search_query='
    URL+=modifiedMovieNameForURL
    URL+='+trailer'

    # now we just access that URL
    html=requests.get(URL)
    soup = BeautifulSoup(html.text, 'html.parser')

    print(soup.prettify())'''

    searchResult = VideosSearch(movieName+" trailer", limit=1)
    #print(searchResult.result())
    id = searchResult.result()['result'][0]['id']
    embedLink = 'https://www.youtube.com/embed/'
    embedLink+=id
    #print(embedLink)
    
    return embedLink
