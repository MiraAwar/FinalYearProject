import React, { useEffect, useState } from 'react';
import { Chart } from 'chart.js/auto';

function Graph() {
  const [chartData, setChartData] = useState(null);

  useEffect(() => {
    // TODO: Fetch data from Flask backend API
    // Example: fetch('/api/data').then(response => response.json()).then(data => setChartData(data));

    // Example chart data (replace with real data):
    setChartData({
      labels: ['January', 'February', 'March', 'April', 'May', 'June', 'July'],
      datasets: [
        {
          label: 'Sales',
          data: [65, 59, 80, 81, 56, 55, 40],
          backgroundColor: 'rgba(75,192,192,0.2)',
          borderColor: 'rgba(75,192,192,1)',
          borderWidth: 1,
        },
      ],
    });
  }, []);

  useEffect(() => {
    if (chartData) {
      const chartCanvas = document.getElementById('myChart');
      const myChart = new Chart(chartCanvas, {
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
    }
  }, [chartData]);

  return (
    <div className='graph'>
      <canvas id="myChart"></canvas>
    </div>
  );
}

export default Graph;