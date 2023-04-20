import React, { useEffect, useState } from 'react';
import logo from './logo.svg';
import './App.css';
import LoginButton from './components/LoginButton';
import FileUpload from './components/FileUpload';
import Graph from './components/Graph';


function App() {
  const [sharedState, setSharedState] = useState(false);
  const myArray = [1,2,3,4,5,6,7];
  return (
    <div>
      <div className="App" hidden={sharedState}>
      <header className="main-header">
        <img src={logo} className="App-logo" alt="logo" />
        <p>
          Welcome! This is our financial web-app. <br></br>
          Upload your CSV file of bond prices to process. <br></br>
        </p>
        {/* <LoginButton /> */}
        <FileUpload sharedState={sharedState} setSharedState={setSharedState} />
      </header>
      </div>
      <div hidden={!sharedState}>
        <header className="in-app-header">
          <p>
            Your graph is processed!<br></br>
            Check your maturity and price forecasting. <br></br>
          </p>
        </header>
        <br></br>
        <br></br>
        <Graph data ={myArray}/>
        <br></br>
        <button className="back" onClick={() => setSharedState(false)}>
        Upload Another File
        </button>
      </div>
    </div>
  );
}

export default App;
