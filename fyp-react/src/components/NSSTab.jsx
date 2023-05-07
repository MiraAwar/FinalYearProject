import React, { useState } from 'react';


const NSSTab = () => {
    
    const [file, setFile] = useState(null)
    const [filename, setFilename] = useState('')
    const [selectedYear, selectedYearValue] = useState('2023');
    const [selectedCalibrate, selectedCalibrateValue] = useState('2021');
    const [apiResponse, setApiResponse] = useState('');
    const [selectedMaturity, selectedMaturityValue] = useState('1');
    
    const handleYearSelectChange = (event) => {
        selectedYearValue(event.target.value);
    }

    const handleCalibrateSelectChange = (event) => {
        selectedCalibrateValue(event.target.value);
    }
    
    const handleMaturitySelectChange = (event) => {
        selectedMaturityValue(event.target.value);
    }

    function processFile(file) {
        setFile(file);
        setFilename(file.name);
        uploadFile(file);
    }

    function uploadFile(file) {
        const formData = new FormData();
        formData.append('file', file);
        fetch("http://localhost:5000//upload_file", {
            method: 'POST',
            body: formData
        })
        .then(response => response.json())
    }
    
    const handleCalibrateButtonClick = () => {
        fetch("http://localhost:5000//nss_calibrate//"+selectedCalibrate+"//"+selectedMaturity)
            .then(response => {
                if (response.ok) {
                    return console.log(response);
                } else {
                    throw new Error('Error: ' + response.status);
                }
            })
          .then(data => {
            setApiResponse(data);
            console.log("the API finished and returned");
            console.log(data);
          })
          .catch(error => {
            console.error(error);
          });
      }
    
      const handlePredictValueButtonClick = () => {
        fetch("http://localhost:5000//nss_predict_value//"+selectedYear+"//"+selectedMaturity)
            .then(response => {
                if (response.ok) {
                    return console.log(response);
                } else {
                    throw new Error('Error: ' + response.status);
                }
            })
          .then(data => {
            setApiResponse(data);
            console.log("the API finished and returned");
            console.log(data);
          })
          .catch(error => {
            console.error(error);
          });
      }

      const handlePredictArrayButtonClick = () => {
        fetch("http://localhost:5000//nss_predict_array//"+selectedYear+"//"+selectedMaturity)
            .then(response => {
                if (response.ok) {
                    return console.log(response);
                } else {
                    throw new Error('Error: ' + response.status);
                }
            })
          .then(data => {
            setApiResponse(data);
            console.log("the API finished and returned");
            console.log(data);
          })
          .catch(error => {
            console.error(error);
          });
      }


    return (
        <div>
            <h2 className="content__title">Run a modified version of the NSS algorithm that can graph you the yearly bond yield.
                    Choose your desired year and maturity bounded needed.</h2>
            <div className='content__tab1'>
                <label>Calibrate for year:</label>
                <select value={selectedCalibrate} onChange={handleCalibrateSelectChange}>
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
                <label className='select_label'>Predict for year:</label>
                <select value={selectedYear} onChange={handleYearSelectChange}>
                    <option value="kaza" disabled>Choose Year</option>
                    <option value="2023">2023</option>
                    <option value="2023">2024</option>
                    <option value="2023">2025</option>
                    <option value="2023">2030</option>
                    <option value="2023">2035</option>
                    <option value="2023">2040</option>
                    <option value="2023">2045</option>
                    <option value="2023">2050</option>
                </select>
                <label className='select_label'>and for Maturity:</label>
                <select value={selectedMaturity} onChange={handleMaturitySelectChange}>
                <option value="kaza" disabled>Choose Maturity</option>
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
                    <option value="13">13</option>
                    <option value="16">16</option>
                    <option value="20">20</option>
                    <option value="25">25</option>
                    <option value="30">30</option>
                    <option value="35">35</option>
                    <option value="40">40</option>
                    <option value="45">45</option>
                    <option value="50">50</option>
                </select>
            </div>
            <br></br>
            <div className="buttons">
                <button className="button button-primary" onClick={handleCalibrateButtonClick}>Calibrate</button>
                <button className="button button-secondary" onClick={handlePredictValueButtonClick}>Forecast Weighted Average</button>
                <button className="button button-primary" onClick={handlePredictArrayButtonClick}>Forecast Individual Maturity</button>
            </div>
            <br></br>
            {/* <p>The Api response: {apiResponse}</p>
            <p>Selected calibration: {selectedCalibrate}</p>
            <p>Selected year: {selectedYear}</p>
            <p>Selected maturity: {selectedMaturity}</p> */}
        </div>
    )
}

export default NSSTab;