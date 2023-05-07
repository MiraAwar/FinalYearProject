import React, { useState } from 'react';

const MonteCarloTab = () => {

    const [file, setFile] = useState(null)
    const [filename, setFilename] = useState('')
    const [apiResponse, setApiResponse] = useState('');
    const [days, setDays] = useState(1);
    const handleDaySelectChange = (event) => {
        setDays(event.target.value);
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

      const handleMonteCarloDefaultButtonClick = () => {
        fetch("http://localhost:5000//monte_carlo_default//"+days)
        .then(response => {
            if (response.ok) {
                return response.blob();
            } else {
                throw new Error('Error: ' + response.status);
            }
        })
        .then(data => {
            const url = window.URL.createObjectURL(new Blob([data]));
            const link = document.createElement('a');
            link.href = url;
            link.setAttribute('download', 'output.xlsx');
            document.body.appendChild(link);
            link.click();
        })
        .catch(error => {
            console.error(error);
        });
      }

      const handleMonteCarloCSVButtonClick = (monte_carlo_csv_file_name) => {
        fetch("http://localhost:5000//monte_carlo//"+monte_carlo_csv_file_name+"//"+days)
        .then(response => {
            if (response.ok) {
                return response.blob();
            } else {
                throw new Error('Error: ' + response.status);
            }
        })
        .then(data => {
            const url = window.URL.createObjectURL(new Blob([data]));
            const link = document.createElement('a');
            link.href = url;
            link.setAttribute('download', 'output.xlsx');
            document.body.appendChild(link);
            link.click();
        })
        .catch(error => {
            console.error(error);
        });
      }

return(
    <div>
        <h2 className="content__title">Execute a Monte-Carlo Simulation that predicts your CSV file maturities,
                    or just use one of our own default bond yield files.</h2>
        <div className='content__tab2'>
            <label for="days">Predict Amount of Days:</label>
            <select value={days} onChange={handleDaySelectChange}>
                <option value="kaza" disabled>Choose Number of Days</option>
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
                <option value="50">60</option>
                <option value="50">70</option>
                <option value="50">80</option>
                <option value="50">90</option>
                <option value="50">100</option>
            </select>
            <label for="monte-carlo-file-upload" class="content__file--upload">
                {file ? file.name : 'Upload File'}
            </label>
            <input name="file" id="monte-carlo-file-upload" accept="text/csv" type="file" onChange={
            (e) => processFile(e.target.files[0])
        }/>
        </div>
        <div className="buttons">
        <button className="button button-primary" onClick={handleMonteCarloDefaultButtonClick}>Default Prediction</button>
        <button className="button button-secondary" onClick={ () => handleMonteCarloCSVButtonClick(filename)}>Predict Your CSV</button>
        </div>
    </div>
)}

export default MonteCarloTab;