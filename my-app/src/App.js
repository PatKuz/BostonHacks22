import logo from './logo.svg';
import './App.css';
import Webcam from "react-webcam";
import { useState, useEffect } from 'react'
import axios from "axios"
import React from 'react';

const videoConstraints = {
  width: 1920,
  height: 1080,
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
  const [webcam, setWebcam] = React.useState(true);

  

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

  const capture = React.useCallback(() => {
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
  }, [webcamRef, setImgSrc]);

  const endCapture = () => {
    setWebcam(false);
  };

  useEffect(() => {
    const interval = setInterval(() => capture(), 1000);
    return () => clearInterval(interval);
  }, []);

  return (
    <div className="App">
      <header className="App-header">
        {/* <button onClick={capture}>Capture photo</button> */}
        <div style={{marginTop: '50px', marginBottom: '20000px'}}>
          {imgSrc && (
            <img
              src={imgSrc}          
            />)
          }
          <div>
            <button onClick={endCapture}>End Drive</button>
          </div>
        </div>
      </header>
      {webcam &&
        <Webcam
          muted={false}
          ref={webcamRef}
          screenshotFormat="image/jpeg"
          // videoConstraints={videoConstraints}
        />
      }
    </div>
  );
}


export default App;
