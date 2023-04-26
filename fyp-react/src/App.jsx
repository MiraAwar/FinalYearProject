import React, { useState } from 'react';
import Circles from './Circles';
import './App.css';

const App = () => {

    const [tab, setTab] = useState(1);
    const [file, setFile] = useState(null)
    const [selectedYear, selectedYearValue] = useState('2014');
    const handleYearSelectChange = (event) => {
        // Update the state with the selected value
        selectedYearValue(event.target.value);
    }
    
    const [selectedMaturity, selectedMaturityValue] = useState('1');
    const handleMaturitySelectChange = (event) => {
        // Update the state with the selected value
        selectedMaturityValue(event.target.value);
    }
    
    const [apiResponse, setApiResponse] = useState('');
    const handleCalibrateButtonClick = () => {
        // Call the API or perform any asynchronous operation here
        fetch("http://localhost:5000//nss_calibrate//"+selectedYear+"//"+selectedMaturity)
            .then(response => {
                if (response.ok) {
                    return console.log(response);;  // Parse the response as JSON
                } else {
                    throw new Error('Error: ' + response.status);
                }
            })
          .then(data => {
            // Update the state with the API response
            setApiResponse(String(data));
            console.log("the API finished and returned");
            console.log(String(data));
          })
          .catch(error => {
            // Handle any errors here
            console.error(error);
          });
      }

      const handleNNDefaultButtonClick = () => {
        // Call the API or perform any asynchronous operation here
        fetch("http://localhost:5000//neural_network_default")
            .then(response => {
                if (response.ok) {
                    return console.log(response);;  // Parse the response as JSON
                } else {
                    throw new Error('Error: ' + response.status);
                }
            })
          .then(data => {
            // Update the state with the API response
            setApiResponse(String(data));
            console.log("the API finished and returned");
            console.log(String(data));
          })
          .catch(error => {
            // Handle any errors here
            console.error(error);
          });
      }

    function changeTab(num) {
        setTab(num);
        let arr = document.getElementsByClassName('tab')
        Array.from(arr).forEach((item) => {
            item.classList.remove('active')
        })
        arr[num - 1].classList.add('active')
    }

    return (
        <div id="app">
            <div className="app__container">
                <h1 className="app__title">Bond Yield Processor</h1>
                <div className="tabs">
                    <h2 className="tab active" onClick={
                        () => changeTab(1)
                    }>NSS Algorithm</h2>
                    <h2 className="tab" onClick={
                        () => changeTab(2)
                    }>Monte-Carlo Simulation</h2>
                    <h2 className="tab" onClick={
                        () => changeTab(3)
                    }>Neural-Network Model</h2>
                </div>
                <div className="content">
                    
                    {
                        tab === 1 ? (
                            <div>
                                <h2 className="content__title">Run a modified version of the NSS algorithm that can graph you the yearly bond yield.
                                        Choose your desired year and maturity bounded needed.</h2>
                                <div className='content__tab1'>
                                    <select value={selectedYear} onChange={handleYearSelectChange}>
                                        <option value="kaza" disabled>Choose Year</option>
                                        <option value="2014">2014</option>
                                        <option value="2015">2015</option>
                                        <option value="2016">2016</option>
                                        <option value="2017">2017</option>
                                        <option value="2018">2018</option>
                                        <option value="2019">2019</option>
                                        <option value="2020">2020</option>
                                        <option value="2021">2021</option>
                                        <option value="2022">2022</option>
                                        <option value="2023">2023</option>
                                    </select>
                                    <select value={selectedMaturity} onChange={handleMaturitySelectChange}>
                                        <option value="kaza" disabled>Choose Maturity Bound</option>
                                        <option value="1">1</option>
                                        <option value="2">2</option>
                                        <option value="3">3</option>
                                        <option value="4">4</option>
                                        <option value="5">5</option>
                                        <option value="6">6</option>
                                        <option value="7">7</option>
                                        <option value="8">8</option>
                                        <option value="9">9</option>
                                        <option value="10">10</option>
                                    </select>
                                </div>
                                <br></br>
                                <div className="buttons">
                                    <button className="button button-primary" onClick={handleCalibrateButtonClick}>Calibrate</button>
                                    <button className="button button-secondary">Forecast</button>
                                </div>
                                <br></br>
                                <p>Selected value: {selectedYear}</p>
                                <p>Selected value: {selectedMaturity}</p>
                                <div>
                                    <p>The Api response: {apiResponse}</p>
                                </div>
                            </div>
                        ) : (
                            tab === 2 ? (
                                <div>
                                    <h2 className="content__title">Execute a Monte-Carlo Simulation that predicts your CSV file maturities,
                                                or just use one of our own default bond yield files.</h2>
                                    <div className='content__tab2'>
                                        <label for="file-upload" class="content__file--upload">
                                            {file ? file.name : 'Upload File'}
                                        </label>
                                    </div>
                                    <div className="buttons">
                                    <button className="button button-primary">Default Prediction</button>
                                    <button className="button button-secondary">Predict Your CSV</button>
                                </div>
                                </div>
                            ) : (
                                <div>
                                    <h2 className="content__title">Run the model to predict your maturities on your own CSV file,
                                                or just use one of our own default bond yield files.</h2>
                                    <div className='content__tab2'>
                                        <label for="file-upload" class="content__file--upload">
                                            {file ? file.name : 'Upload File'}
                                        </label>
                                    </div> 
                                    <div className="buttons">
                                    <button className="button button-primary" onClick={handleNNDefaultButtonClick}>Default Prediction</button>
                                    <button className="button button-secondary">Predict Your CSV</button>
                                </div>
                                </div>
                            )
                               
                        )
                    }                                
                    
                    <input id="file-upload" accept="text/csv" type="file" onChange={
                        (e) => setFile(e.target.files[0])
                    }/>
                </div>
            </div>
            <Circles />
        </div>
    );
}

export default App;