

const ctx = document.getElementById('myChart').getContext('2d');

var graph_data = {
    type: 'line',

    data: {
        labels: ['Red', 'Blue', 'Yellow', 'Green', 'Purple', 'Orange'],
        datasets: [{
            label: '# of Votes',
            data: [12, 19, 3, 5, 2, 3],
            tension: 0,
            backgroundColor: [
                'rgba(255, 99, 132, 0.2)',

            ],

            borderWidth: 5
        }]
    },
  

}
const data = {
  labels: ['January', 'February', 'March', 'April', 'May', 'June', 'July'],
  datasets: [{
    label: 'Looping tension',
    data: [65, 59, 80, 81, 26, 55, 40],
    tension: 0.5,
    fill: false,
    borderColor: 'rgb(75, 192, 192)',
  }]
};

const config = {
    type: 'line',
    data: graph_data,
    bezierCurve: true,
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
        }
      }
    }
  };


const myChart = new Chart(ctx, graph_data, config);



var socket = new WebSocket('ws://localhost:8000/ws/graph/')

socket.onmessage = function(e){
    var djangoData = JSON.parse(e.data);
    console.log(djangoData);
    
     var newGraphData = graph_data.data.datasets[0].data;
     newGraphData.shift();
     newGraphData.push(djangoData.value);

     graph_data.data.datasets[0].data = newGraphData;
     myChart.update();

}