import React, { useState } from 'react';

const MonteCarloTab = () => {

    const [tab, setTab] = useState(1);
    const [file, setFile] = useState(null)
    const [filename, setFilename] = useState('')
    const [apiResponse, setApiResponse] = useState('');

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
        fetch("http://localhost:5000/monte_carlo_default")
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
        fetch("http://localhost:5000//monte_carlo//"+monte_carlo_csv_file_name)
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
        <br></br>
        <p>The Api response: {apiResponse}</p>
    </div>
)}

export default MonteCarloTab;