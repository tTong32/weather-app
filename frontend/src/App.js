import React from 'react';
import Header from './components/Header';
import CurrentWeather from './components/CurrentWeather';
import Forecast from './components/Forecast';
import WeatherHistory from './components/WeatherHistory';
import PMAInfo from './components/PMAInfo';
import './App.css';

function App() {
  return (
    <div className="App">
      <Header />
      <main>
        <CurrentWeather />
        <Forecast />
        <WeatherHistory />
      </main>
      <PMAInfo />
    </div>
  );
}

export default App;
