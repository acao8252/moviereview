from utils.utils import get_soup

def scrape():
	url = 'https://www.metacritic.com/browse/movies/release-date/theaters/date?ttype=1&view=detailed'
	metasoup = get_soup(url)
	metasoup_list = metasoup.find_all("td", class_="clamp-summary-wrap")
	movie_list = list()
	for movies in metasoup_list:
		#scrape the movie names
		title = movies.find('h3').text
		#scrape the release_dates
		release_date = movies.select('div.clamp-details span')[0].text
		#scrape the user scores.
		if (movies.select('a.metascore_anchor div')[2].text == "tbd"):
			score = 0
			votes = 0
		else:
			score = int((float((movies.select('a.metascore_anchor div')[2]).text))*10)
			movie_in_url = (title.replace(': ', '-').replace(' ', '-').replace("'", '')).lower()
			movie_url = 'https://www.metacritic.com/movie/' + movie_in_url
			print(movie_url)
			moviesoup = get_soup(movie_url).find_all("span", {"class": "based_on"})[1].get_text(strip=True)
			moviesoup = int(''.join(filter(str.isdigit, moviesoup)))
			votes = moviesoup
		movie_data = {
		    "title": title,
		    "score": score,
		    "votes": votes,
		}
		movie_list.append(movie_data)
	return movie_list
