import React, { useState } from 'react';
import Table from "./Table";

const RFRTab = () => {

    const [file, setFile] = useState(null)
    const [filename, setFilename] = useState('')
    const [apiResponse, setApiResponse] = useState('');

    const [selectedMaturity, selectedMaturityValue] = useState('1');
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

    const handleRFRDefaultButtonClick = () => {
        fetch("http://localhost:5000//rfr_predict_default//"+selectedMaturity)
            .then(response => {
                if (response.ok) {
                    return response.json();
                } else {
                    throw new Error('Error: ' + response.status);
                }
            })
          .then(data => {
            setApiResponse(Object.values(data));
            console.log("the API finished and returned");
            console.log(data);
          })
          .catch(error => {
            console.error(error);
          });
      }

    const handleRFRCSVButtonClick = (csv_file_name) => {
        fetch("http://localhost:5000//rfr_predict//"+csv_file_name+"//"+selectedMaturity)
            .then(response => {
                if (response.ok) {
                    return response.json();
                } else {
                    throw new Error('Error: ' + response.status);
                }
            })
            .then(data => {
            setApiResponse(Object.values(data));
            console.log("the API finished and returned");
            console.log(data);
            })
            .catch(error => {
            console.error(error);
        });
    }
      
return(
    <div>
        <h2 className="content__title">Run the Random Forest Regressor model to predict yields of your own CSV,
                    or just use one of our own default bond yield files.</h2>
        <div className='content__tab4'>
            <label>Predict for maturity (years):</label>
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
            <label for="rfr-file-upload" class="content__file--upload">
                {file ? file.name : 'Upload File'}
            </label>
        </div> 
        <input name="file" id="rfr-file-upload" accept="text/csv" type="file" onChange={
            (e) => processFile(e.target.files[0])
        }/>
        <div className="buttons">
        <button className="button button-primary" onClick={handleRFRDefaultButtonClick}>Default Prediction</button>
        <button className="button button-secondary" onClick={() => handleRFRCSVButtonClick(filename)}>Predict Your CSV</button>
        </div>
        <br></br>
        <label className='result_label'>RESULT:</label>
        <div>
            <Table data={apiResponse} maturity={selectedMaturity} />
        </div>
    </div>
)}

export default RFRTab;