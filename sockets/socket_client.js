var exampleSocket = new WebSocket("192.168.43.68:65432");

exampleSocket.onmessage = function (event) {
    console.log(event.data);
  }