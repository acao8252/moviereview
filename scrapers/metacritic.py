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
		#scrape the meta scores
		score = int(movies.select('a.metascore_anchor div')[0].text)
		#scrape the user scores.
		votes = int(movies.select('a.metascore_anchor div')[2].text)
		movie_data = {
		    "title": title,
		    "score": score,
		    "votes": votes,
		}
		movie_list.append(movie_data)
	return movie_list
