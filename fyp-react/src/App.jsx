import React, { useState } from 'react';
import Circles from './Circles';
import './App.css';
import NSSTab from './components/NSSTab';
import MonteCarloTab from './components/MonteCarloTab';
import NNTab from './components/NNTab';
import StockTab from './components/StockTab';
import ExchangeTab from './components/ExchangeTab';
import RFRTab from './components/RFRTab';

const App = () => {

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

      const handleMissingDataButtonClick = (csv_file_name) => {
        fetch("http://localhost:5000//impute_missing_data//"+csv_file_name)
            .then(response => {
                if (response.ok) {
                    return response.json();
                } else {
                    throw new Error('Error: ' + response.status);
                }
            })
          .then(data => {
            const url = window.URL.createObjectURL(new Blob([data]));
            const link = document.createElement('a');
            link.href = url;
            link.setAttribute('download', csv_file_name);
            document.body.appendChild(link);
            link.click();
          })
          .catch(error => {
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
                <div className="floater">
                    <h3 className='missing-data-label'>Does your file contain missing data? Upload, and click the button to fix the missing data.</h3>
                    <label for="missing-data-file-upload" class="missing-data__file--upload">
                        {file ? file.name : 'Upload File'}
                    </label>
                    <input name="file" id="missing-data-file-upload" accept="text/csv" type="file" onChange={
                        (e) => processFile(e.target.files[0])
                    }/>
                    <br/>
                    <button className="button button-side" onClick={ () => handleMissingDataButtonClick(filename)}>Compute Missing Data</button>
                </div>
                <h1 className="app__title">Bond Yield Processor</h1>
                <div className="tabs">
                    <h2 className="tab active" onClick={
                        () => changeTab(1)
                    }>NSS Yield Algorithm</h2>
                    <h2 className="tab" onClick={
                        () => changeTab(2)
                    }>Monte-Carlo Yield Simulation</h2>
                    <h2 className="tab" onClick={
                        () => changeTab(3)
                    }>Yield Neural-Network Model</h2>
                    <h2 className="tab" onClick={
                        () => changeTab(4)
                    }>RFR Yield Prediction</h2>
                    <h2 className="tab" onClick={
                        () => changeTab(5)
                    }>Exchange Rate Prediction</h2>
                    <h2 className="tab" onClick={
                        () => changeTab(6)
                    }>Stock Price Prediction</h2>
                </div>
                <div className="content">
                    { tab === 1 && <NSSTab /> }
                    { tab === 2 && <MonteCarloTab /> }
                    { tab === 3 && <NNTab /> }
                    { tab === 4 && <RFRTab /> }
                    { tab === 5 && <ExchangeTab /> }
                    { tab === 6 && <StockTab /> }
                </div>
            </div>
            <Circles />
        </div>
    );
}

export default App;