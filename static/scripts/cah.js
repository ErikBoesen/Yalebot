/*
onclick = function(e) {
    console.log("Clicked somewhere.");
    if (e.target.classList.contains("card") && e.target.classList.contains("white")) {
        console.log("Clicked on a card.");
        var cardIndex = Array.prototype.indexOf.call(e.target.parentNode.children, e.target);

        var req = new XMLHttpRequest();
        req.open("POST", location.href);
        req.setRequestHeader("Content-Type", "application/json;charset=UTF-8");
        var url = new URL(location.href);
        var data = {
            "access_token": url.searchParams.get("access_token"),
            "card_index": cardIndex,
        };
        req.send(JSON.stringify(data));
        req.onreadystatechange = function() {
            if (this.readyState == 4 && this.status == 200) {
                location.reload();
            }
        };
    }
};
*/
var url = new URL(location.href);
var access_token = url.searchParams.get("access_token");

var socket = io.connect(location.protocol + "//" + location.host);
socket.on("connect", function() {
    socket.emit("cah_connect", {"access_token": access_token});
});
