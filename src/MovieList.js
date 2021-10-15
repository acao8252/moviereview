import React, { Component } from 'react'
import moviedata from './scrapers/imdbScrape15-10-2021.json'
import moviedata2 from './scrapers/rottenTomatoesScrape13-10-2021.json'
class MovieList extends Component {
	render() {
      return (
        <div>
          <h1>Ranking for IMDB</h1>
          {moviedata.map((movieDetail,  index)=>{
          	return <h1>{movieDetail}</h1>
          })}
          <br></br><br></br>

          <h1>Ranking for Rotten Tomatoes</h1>
          {moviedata.map((movieDetail2,  index)=>{
          	return <h1>{movieDetail2}</h1>
          })}
        </div>
      )
	}
}

export default MovieList