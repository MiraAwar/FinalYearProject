import React, { useState } from 'react';

const ExchangeTab = () => {

    const [file, setFile] = useState(null);
    const [date, setDate] = useState('05-06-2023');
    const [fromCurrency, setFromCurrency] = useState('EUR');
    const [toCurrency, setToCurrency] = useState('USD');
    const [filename, setFilename] = useState('');
    const [apiResponse, setApiResponse] = useState('');

    const handleDateSelectChange = (event) => {
        setDate(event.target.value);
    }

    const handleFromCurrencySelectChange = (event) => {
        setFromCurrency(event.target.value);
    }

    const handleToCurrencySelectChange = (event) => {
        setToCurrency(event.target.value);
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

    const handleExchangeDefaultButtonClick = () => {
        fetch("http://localhost:5000//exchange_predict_default//"+date+"//"+fromCurrency+"//"+toCurrency)
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

      const handleExchangeButtonClick = (csv_file) => {
        fetch("http://localhost:5000//exchange_predict//"+date+"//"+csv_file)
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
        <h2 className="content__title">Run the Vector Auto-Regression model to predict exchange rates for the selected day.</h2>
        <div className='content__tab5'>
            <label for="date">Predict for Date:</label>
            <select value={date} onChange={handleDateSelectChange}>
                <option value="kaza" disabled>Choose Date</option>
                <option value="05-06-2023">05-06-2023</option>
                <option value="05-07-2023">05-07-2023</option>
                <option value="05-08-2023">05-08-2023</option>
                <option value="05-09-2023">05-09-2023</option>
                <option value="05-10-2023">05-10-2023</option>
                <option value="05-11-2023">05-11-2023</option>
                <option value="05-12-2023">05-12-2023</option>
                <option value="05-13-2023">05-13-2023</option>
                <option value="05-14-2023">05-14-2023</option>
                <option value="05-15-2023">05-15-2023</option>
                <option value="05-16-2023">05-16-2023</option>
                <option value="05-17-2023">05-17-2023</option>
                <option value="05-18-2023">05-18-2023</option>
                <option value="05-19-2023">05-19-2023</option>
                <option value="05-20-2023">05-20-2023</option>
                <option value="06-23-2023">06-23-2023</option>
                <option value="07-05-2023">07-05-2023</option>
                <option value="09-30-2023">09-30-2023</option>
                <option value="12-12-2023">12-12-2023</option>
                <option value="05-05-2024">05-05-2024</option>
                <option value="05-05-2025">05-05-2025</option>
            </select>
            <label className='select_label' for="from">Choose Currency from:</label>
            <select value={fromCurrency} onChange={handleFromCurrencySelectChange}>
                <option value="kaza" disabled>Choose Currency from</option>
                <option value="EUR">EUR</option>
                <option value="JPY">JPY</option>
                <option value="INR">INR</option>
                <option value="GBP">GBP</option>
                <option value="MXN">MXN</option>
                <option value="CAD">CAD</option>
            </select>
            <label className='select_label' for="to">Choose Currency to:</label>
            <select value={toCurrency} onChange={handleToCurrencySelectChange}>
                <option value="kaza" disabled>Choose Currency to</option>
                <option value="USD">USD</option>
            </select>
            <label for="exchange-file-upload" class="content__file--upload">
                {file ? file.name : 'Upload File'}
            </label>
            <input name="file" id="exchange-file-upload" accept="text/csv" type="file" onChange={
            (e) => processFile(e.target.files[0])
        }/>
        </div> 
        <div className="buttons">
            <button className="button button-primary" onClick={handleExchangeDefaultButtonClick}>Default Exchange Rate Prediction</button>
            <button className="button button-secondary" onClick={ () => handleExchangeButtonClick(filename)}>Predict Your CSV</button>
        </div>
        <br></br>
        <label className='result_label'>RESULT: ${apiResponse}</label>
    </div>
)}

export default ExchangeTab;