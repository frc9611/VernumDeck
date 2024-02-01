$(document).ready(function () {
    //connect to the socket server.
    //   var socket = io.connect("http://" + document.domain + ":" + location.port);
    var socket = io.connect();
  
    //receive details from server
    socket.on("updateData", function (msg) {
      console.log("a")
      kv = msg.kv.split("::")
      console.log("Received data :: " + msg.date + " :: " + kv);      
      let doc;

      if(document.getElementById(kv[0]) == 0) {doc = document.createElement("p"); document.body.appendChild(doc)}
      else doc = document.getElementById(kv[0])

      doc.id = kv[0]
      let node = document.createTextNode(`${kv[0]}: ${kv[1]} - Atualizado em ${msg.date}`)
      doc.replaceChildren(node)
    });
  });