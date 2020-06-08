function initSocketIO(namespace) {
    console.log("document.location.href is: " + document.location.href);
    socket = io.connect(document.location.origin +
        "/" + namespace); //("ws://" + document.location.hostname + document.location.port);
    // socket = io.connect("ws://" + document.location.hostname + document.location.port + "/test");


}








function send_score_update(chosenGusesser) {
    socket.emit("point_given_to", chosenGusesser)
}

function send_drawn(draw_data) {
    socket.emit("pt", draw_data)
}