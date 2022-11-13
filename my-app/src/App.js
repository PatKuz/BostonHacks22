import logo from './logo.svg';
import './App.css';
import Webcam from "react-webcam";
import { useState, useEffect } from 'react'
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

  

  // const soundTheAlarms = (() => {
  //   console.log('change things here')
  // })

  const updateStuff = React.useCallback( async (asleep, image) => {
    console.log('updating stuff')
    setImgSrc(image)
    if (asleep){
      // soundTheAlarms()
    }
  }, [setImgSrc])

  const turningOffRunning = React.useCallback(async () => {
    setRunning(false);
  }, [setRunning])

  const turnOnRunning = React.useCallback(() => {
    setRunning(true);
  }, [setRunning])

  // const updateStuff = (asleep, image) = (async (asleep, image) => {
  //   console.log('updating stuff')
  //   setImgSrc(image)
  //   if (asleep){
  //     soundTheAlarms()
  //   }
  // }, [imgSrc])

  const capture = React.useCallback(async () => {
    console.log('this is running')
    // turnOnRunning()
    setRunning(true)
    // var temp_running = true
    // running = true
    // console.log('running start: ' + running)
    // while(running){
    //   console.log('running: ' + running)
    //   console.log('in loop')
    //   const imageSrc = webcamRef.current.getScreenshot();
    //   console.log('in here')
    //   console.log(imageSrc)
    //   // setImgSrc(imageSrc);

    //   axios.post('/live', {
    //     name: 'Conor',
    //     imageSrc: imageSrc,
    //   })
    //   .then((response) => {
    //     console.log('response')
    //     console.log(response)
    //     const asleep = response['data']['asleep']
    //     console.log('asleep')
    //     console.log(asleep)
    //     const imageSrc = response['data']['image']
    //     updateStuff(asleep, imageSrc)

    //   }).catch((error) => {
    //     console.log('got an error')
    //     console.log(error)
    //   })
      
    //   await sleep(100);
    //   console.log('running end: ' + running)
    //   break;


    // }
    

  }, [setRunning]);

  const endCapture = React.useCallback(async () => {
    console.log('ending the drive');
    setRunning(false);
  }, [setRunning]);

  useEffect(() => {
    while(running){
      console.log('running: ' + running)
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
        console.log('response')
        console.log(response)
        const asleep = response['data']['asleep']
        console.log('asleep')
        console.log(asleep)
        const imageSrc = response['data']['image']
        updateStuff(asleep, imageSrc)
  
      }).catch((error) => {
        console.log('got an error')
        console.log(error)
      })
      
      const sleep = ms => new Promise(
        resolve => setTimeout(resolve, ms)
      );
      sleep(10000)
      console.log('running end: ' + running)
      break;
  
  
    }
  });

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
      <button onClick={endCapture}>End Drive</button>
      {imgSrc && (
        <img
          src={imgSrc}
        />)}
      </header>
    </div>
  );
}


export default App;
