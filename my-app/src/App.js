import logo from './logo.svg';
import './App.css';
import Webcam from "react-webcam";
import { useState } from 'react'
import axios from "axios"

const videoConstraints = {
  width: 1280,
  height: 720,
  facingMode: "user"
};


function getData() {
  var screenshot = this.webcam.current.getScreenshot();
  console.log(screenshot.toString())
  console.log('image src')
  // console.log(imageSrc)

  axios.post('/live', {
    name: 'Conor'
  })
  .then((response) => {
    console.log('got a response')
  }).catch((error) => {
   console.log('got an error')
  })
}

// const WebcamCapture = () => (
// );


function App() {
  return (
    <div className="App">
      <header className="App-header">
        <img src={logo} className="App-logo" alt="logo" />
        <p>
          Edit <code>src/App.js</code> and save to reload.
        </p>
        <a
          className="App-link"
          href="https://reactjs.org"
          target="_blank"
          rel="noopener noreferrer"
        >
          Learn React
        </a>
        <Webcam
    audio={false}
    height={720}
    screenshotFormat="image/jpeg"
    width={1280}
    videoConstraints={videoConstraints}
  >
    {({ getScreenshot }) => (
      <button
        onClick={() => {getData()}}
      >
        Capture photo
      </button>
    )}
  </Webcam>
      </header>
    </div>
  );
}


export default App;
