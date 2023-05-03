import React, { useState } from 'react';


const NSSTab = () => {

    const [file, setFile] = useState(null)
    const [filename, setFilename] = useState('')
    const [selectedYear, selectedYearValue] = useState('2014');
    const handleYearSelectChange = (event) => {
        selectedYearValue(event.target.value);
    }
    
    const [selectedMaturity, selectedMaturityValue] = useState('1');
    const handleMaturitySelectChange = (event) => {
        selectedMaturityValue(event.target.value);
    }
    
    const [apiResponse, setApiResponse] = useState('');
    const handleCalibrateButtonClick = () => {
        fetch("http://localhost:5000//nss_calibrate//"+selectedYear+"//"+selectedMaturity)
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

    return (
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
            <p>The Api response: {apiResponse}</p>
            <p>Selected year: {selectedYear}</p>
            <p>Selected maturity: {selectedMaturity}</p>
        </div>
    )
}

export default NSSTab;