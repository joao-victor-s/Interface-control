var data_array = []
var label_array = []

var graph_data = {
    type: 'line',
    data: { 
            labels: Array.from(Array(100).keys()),
            datasets: [{
            label: 'Prototype',
            data: data_array,
            tension: 0.4,
            backgroundColor: 'rgba(255, 99, 132, 0.2)',
            borderWidth: 5
        }]
    },
  

}
const config = {

    type: 'line',
    data: graph_data,
    bezierCurve: true,
    tension: 0.5,
    options: {
      animations: {
        tension: {
          duration: 1000,
          easing: 'easeInSine',
          loop: true
        }
      },
      scales: {
        y: { // defining min and max so hiding the dataset does not change scale range
          min: 0,
          max: 100
        },
        x: {
          type: 'time',
          ticks: {
              autoSkip: true,
              maxTicksLimit: 100
          }
          }
      }
    }
  };

  const ctx = document.getElementById('myChart').getContext('2d');
const myChart = new Chart(ctx, graph_data, config);



var socket = new WebSocket('ws://localhost:7000/ws/graph/')

socket.onmessage = function(e){
    var djangoData = JSON.parse(e.data);
    
     var newGraphData = graph_data.data.datasets[0].data;
     if (newGraphData.length > 99){
        newGraphData.shift();
     }
       
     newGraphData.push(djangoData.value);
     console.log(newGraphData);

     graph_data.data.datasets[0].data = newGraphData;
     myChart.update();

}
