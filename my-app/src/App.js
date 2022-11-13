import logo from './logo.svg';
import './App.css';
import Webcam from "react-webcam";
import { useState } from 'react'
import axios from "axios"
import React from 'react';

const videoConstraints = {
  width: 1280,
  height: 720,
  facingMode: "user"
};



function getData() {
  axios({
    method: "POST",
    url:"/live",
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
  const webcamRef = React.useRef(null);
  const [imgSrc, setImgSrc] = React.useState(null);
  const [running, setRunning] = React.useState(false);

  const sleep = ms => new Promise(
    resolve => setTimeout(resolve, ms)
  );

  const capture = React.useCallback(async () => {
    console.log('this is running')
    setRunning(true)
    // running = true
    console.log(running)
    while(true){
      console.log('in loop')
      const imageSrc = webcamRef.current.getScreenshot();
      console.log('in here')
      console.log(imageSrc)
      // setImgSrc(imageSrc);

      axios.post('/live', {
        name: 'Conor',
        imageSrc: imageSrc,
      })
      .then((response) => {
        console.log('got a response')
      }).catch((error) => {
      console.log('got an error')
      })
      
      await sleep(100);


    }
    

  }, [webcamRef, setImgSrc]);

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
        ref={webcamRef}
        screenshotFormat="image/jpeg"
      />
      <button onClick={capture}>Capture photo</button>
      {imgSrc && (
        <img
          src={imgSrc}
        />)}
      </header>
    </div>
  );
}


export default App;
