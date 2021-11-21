def test():
    scrapersList = [
            "rottenTomatoes",
            "imdb",
            "tmdb",
            "metacritic"
            ]

    testSuccessful = True

    for scraper in scrapersList:

        # this should be a list of dictionary items:
        moviesList = import_module(f"scrapers.{scraper}").scrape()

        testSuccessful = testSuccessful and (type(moviesList)==type([]))

        for movie in moviesList:
            testSuccessful = testSuccessful and (type(movie)==type({'k':'v'}))
    return testSuccessful
