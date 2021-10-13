from datetime import datetime

import json

import requests
from bs4 import BeautifulSoup

from selenium import webdriver
from selenium.webdriver.common.keys import Keys

URL = "https://www.rottentomatoes.com/browse/in-theaters"

now = datetime.now()
dateTimeScraped = now.strftime("%d/%m/%Y %H:%M")
dateScraped = now.strftime("%d-%m-%Y")
#print(dateScraped)

# this part is important because the page uses JS code to generate itself,
# so we actually need to load the page in a browser before continuing
driver=webdriver.Chrome(executable_path=r"C:\Users\jacob\Documents\Personal Files\chromedriver_win32\chromedriver.exe")
driver.get(URL)
elem = driver.find_element_by_class_name("mb-movie")
page_source_text = driver.page_source

# now that we have the raw html of the laoded page, we can handle it using
# our (much more convenient) BeautifulSoup:
rottenTomatoSoup = BeautifulSoup(page_source_text, "html.parser")
content = rottenTomatoSoup.find(id="content-column")
moviesList = content.find_all("div", class_="mb-movie")

scrapedMovieDataList = list()
for moviehtml in moviesList:
    #print(moviehtml.prettify())
    #print("working!")

    scrapedTitle = moviehtml.find("h3", class_="movieTitle").text.strip()

    try:
        scrapedTMeterScore = moviehtml.find("span", class_="tMeterScore").text.strip()
    except Exception:
        continue

    scrapedMovieData = (scrapedTitle, scrapedTMeterScore, dateTimeScraped)
    #print(scrapedMovieData)
    scrapedMovieDataList.append(scrapedMovieData)
#print(scrapedMovieDataList)
print(str(len(scrapedMovieDataList)), "movies scraped")

#okay! We have a list of movies now!

# now we just export to a json file:
with open(('rottenTomatoesScrape'+dateScraped+'.json'), 'w') as f:
    jsonScrapedMovieDataList = json.dump(scrapedMovieDataList, f)
    #print(jsonScrapedMovieDataList)
