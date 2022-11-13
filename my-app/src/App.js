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
  const [asleep, setAsleep] = React.useState(false);

  

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

  const endCaptureBad = () => {
    console.log('Ending the capture')
    setWebcam(false);
    setAsleep(true);
  }


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
        imageSrc: imageSrc,
      })
      .then((response) => {
        console.log('response')
        console.log(response)
        const asleep = response['data']['asleep']
        console.log('asleep')
        console.log(asleep)
        const imageSrc = response['data']['image']
        setImgSrc(imageSrc)
        if(asleep)
          endCaptureBad(asleep, imageSrc)
      }).catch((error) => {
        console.log('got an error')
        console.log(error)
      })
  }, [webcamRef, setImgSrc]);

  const endCapture = () => {
    setWebcam(false);
    axios.post('/end_drive', {
      'hoursDriven': 1000,
    }).then((response) => {
      console.log(response)
    }).catch((error) => {
      console.log('got an error')
      console.log(error)
    })
  };

  
  useEffect(() => {
    const interval = setInterval(() => capture(), 600);
    return () => clearInterval(interval);
  }, []);

  return (
    <div className="App">
      <header className="App-header">
        {/* <button onClick={capture}>Capture photo</button> */}
        
         <div className="roon-wrap">
          <div className="ran-out-of-names">
              We're Live!
          </div>
          <div style={{marginTop: '50px', marginBottom: '2000000px'}}>
          
          <div className="vod">
          {imgSrc && (
            <img
              src={imgSrc}          
            />)
          }
          </div>

          <div>
          {asleep && <p>We have detected you are falling asleep</p> }
        </div>
          
          <div>
            <button onClick={endCapture} className="street-button">End Drive</button>
          </div>
        </div>
        </div>
      </header>

      <div className='vod'>
      {webcam &&
        <Webcam
          muted={false}
          ref={webcamRef}
          screenshotFormat="image/jpeg"
          // videoConstraints={videoConstraints}
        />
      }
      </div>
    </div>
  );
}


export default App;
