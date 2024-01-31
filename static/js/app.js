$(document).ready(function () {
    const ctx = document.getElementById("chart-shooter").getContext("2d");
  
    const chartShooter = new Chart(ctx, {
      type: "line",
      data: {
        datasets: [{ label: "Motor-Shooter Esquerdo",  }],
      },
      options: {
        borderWidth: 3,
        borderColor: ['rgba(255, 99, 132, 1)',],
      },
    });
  
    function addData(label, data) {
      chartShooter.data.labels.push(label);
      chartShooter.data.datasets.forEach((dataset) => {
        dataset.data.push(data);
      });
      chartShooter.update();
    }
  
    function removeFirstData() {
      chartShooter.data.labels.splice(0, 1);
      chartShooter.data.datasets.forEach((dataset) => {
        dataset.data.shift();
      });
    }
  
    const MAX_DATA_COUNT = 10;
    //connect to the socket server.
    //   var socket = io.connect("http://" + document.domain + ":" + location.port);
    var socket = io.connect();
  
    //receive details from server
    socket.on("updateData", function (msg) {
      console.log("Received data :: " + msg.date + " :: " + msg.value);
  
      // Show only MAX_DATA_COUNT data
      if (chartShooter.data.labels.length > MAX_DATA_COUNT) {
        removeFirstData();
      }
      addData(msg.date, msg.value);
    });
  });