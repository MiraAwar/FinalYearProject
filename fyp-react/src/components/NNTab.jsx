import React, { useState } from 'react';

const NNTab = () => {

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
    
    const handleNNDefaultButtonClick = () => {
        fetch("http://localhost:5000//neural_network_default")
            .then(response => {
                if (response.ok) {
                    return response.json();
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

      const handleNNCSVButtonClick = (nn_csv_file_name) => {
        fetch("http://localhost:5000//neural_network//"+nn_csv_file_name)
            .then(response => {
                if (response.ok) {
                    return response.json();
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

return(
    <div>
        <h2 className="content__title">Run the model to predict your maturities on your own CSV file,
                    or just use one of our own default bond yield files.</h2>
        <div className='content__tab3'>
            <label for="nn-file-upload" class="content__file--upload">
                {file ? file.name : 'Upload File'}
            </label>
        </div> 
        <input name="file" id="nn-file-upload" accept="text/csv" type="file" onChange={
            (e) => processFile(e.target.files[0])
        }/>
        <div className="buttons">
        <button className="button button-primary" onClick={handleNNDefaultButtonClick}>Default Prediction</button>
        <button className="button button-secondary" onClick={() => handleNNCSVButtonClick(filename)}>Predict Your CSV</button>
        </div>
        <br></br>
        <p>The Api response: {apiResponse}</p>
    </div>
)}

export default NNTab;