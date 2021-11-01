from utils.utils import get_soup

def scrape():
    url = 'https://www.themoviedb.org/remote/panel?panel=popular_scroller&group=in-theatres&language=en-US'

    soup = get_soup(url)
    raw_movie_list = soup.find_all("div", class_="card style_1")

    movie_list = list()
    for raw_movie in raw_movie_list:
        # movie id to open another page for the votes
        mid = raw_movie.find("div", class_="options")["data-id"]

        title = raw_movie.find("h2").text.strip()
        score = raw_movie.find("div", class_="user_score_chart")["data-percent"]
        score = int(float(score))
        inner_url = f'https://www.themoviedb.org/movie/{mid}/remote/rating/details'
        soup = get_soup(inner_url)
        votes = soup.find("h3").text.strip()

        # turn str "1,340 Ratings" into int "1340"
        votes = votes.replace(" Ratings", "")
        votes = votes.replace(",", "")
        votes = int(votes)

        movie_data = {
                "title": title,
                "score": score,
                "votes": votes,
                }

        # toss that into a superlist
        movie_list.append(movie_data)

    return movie_list
