
var dps = Array(130)

var myChart = new CanvasJS.Chart("chartContainer",{
  title: {
    text: "Live Data"
  },
  axisY: {
    gridThickness: 0
  },
  data: [{
    type: "spline",
    dataPoints: dps
  }]
});
myChart.render();


var socket = new WebSocket('ws://localhost:7000/ws/graph/');
var updateInterval = 500;

socket.onmessage = function(e){
    var djangoData = JSON.parse(e.data);
    console.log(djangoData.value);
    var updatedDps = [];
    myChart.options.data[0].dataPoints = [];

    for(var i = 0; i < dps.length; i++)
      updatedDps.push(djangoData.value[i]);
      console.log(djangoData.value[i]);

    myChart.options.data[0].dataPoints = updatedDps;
    myChart.render();
};
setInterval(function(e){socket.onmessage()}, updateInterval);