import React, { useEffect, useState } from 'react';
import { Chart } from 'chart.js/auto';

function Graph(props) {
  const [chartData, setChartData] = useState(null);
  let myArray = props.data;
  console.log(myArray);

  useEffect(() => {
    // TODO: Fetch data from Flask backend API
    // Example: fetch('/api/data').then(response => response.json()).then(data => setChartData(data));
      
    async function fetchData() {
      const response = await fetch('http://localhost:5000/nss_calibrate/2023/5');
      const jsonData = await response.json();
      console.log(jsonData)
      setChartData(jsonData);
    }
    fetchData();

    // Example chart data (replace with real data):
    const chartData = {
      labels: ['January', 'February', 'March', 'April', 'May', 'June', 'July'],
      datasets: [
        {
          label: 'Sales',
          data: myArray,
          backgroundColor: 'rgba(75,192,192,0.2)',
          borderColor: 'rgba(75,192,192,1)',
          borderWidth: 1,
        },
      ],
    };
    
    setChartData(chartData);
  }, [myArray]);
  

  useEffect(() => {
    if (chartData) {
      const chartCanvas = document.getElementById('myChart');
      let myChart = new Chart(chartCanvas, {
        type: 'bar',
        data: chartData,
        options: {
          scales: {
            yAxes: [
              {
                ticks: {
                  beginAtZero: true,
                  min: 0,
                  max: 100,
                  stepSize: 10
                },
              },
            ],
          },
        },
      });
  
      return () => {
        myChart.destroy();
      };
    }
  }, [chartData]);
  

  return (
    <div className='graph'>
      <p>{JSON.stringify(myArray)}</p>
      <canvas id="myChart"></canvas>
    </div>
  );
}


export default Graph;