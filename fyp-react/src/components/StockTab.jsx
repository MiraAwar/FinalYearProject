import React, { useState } from 'react';

const StockTab = () => {

    const [days, setDays] = useState(1);
    const [stock, setStock] = useState('GOOGL');
    const [apiResponse, setApiResponse] = useState('');

    const handleDaySelectChange = (event) => {
        setDays(event.target.value);
    }

    const handleStockSelectChange = (event) => {
        setStock(event.target.value);
    }

    const handleStockButtonClick = () => {
        fetch("http://localhost:5000//stock_predict//"+stock+"//"+days)
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
        <h2 className="content__title">Run the monte-carlo simulations to predict stock prices for the next days.</h2>
        <div className='content__tab6'>
            <label for="stock">Choose Stock to Predict:</label>
            <select value={stock} onChange={handleStockSelectChange}>
                <option value="kaza" disabled>Choose Stock</option>
                <option value="SPY">SPY</option>
                <option value="AMZN">AMZN</option>
                <option value="GOOGL">GOOGL</option>
            </select>
            <label className='select_label' for="days">Predict Amount of Days:</label>
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
            </select>
        </div> 
        <div className="buttons">
            <button className="button button-primary" onClick={handleStockButtonClick}>Stock Price Prediction</button>
        </div>
        <br></br>
        <label className='result_label'>RESULT: ${apiResponse}</label>
    </div>
)}

export default StockTab;