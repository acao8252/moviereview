import logo from './logo.svg';
import './App.css';
import React from 'react';
import Title from './Title';
import MovieList from './MovieList';


function App() {
  return (
    <div className="App">
      <Title />
        <MovieList />
    </div>
  );
}

export default App;
