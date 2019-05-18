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
// TODO: there is no elegance here. Only sleep deprivation and regret.
// Please, if you have any self-respect, rewrite this entire file.
// Then wipe its inconvenient past from the git history and never speak of it again.
var url = new URL(location.href);
var access_token = url.searchParams.get("access_token");

var socket = io.connect(location.protocol + "//" + location.host);
socket.on("connect", function() {
    socket.emit("cah_connect", {"access_token": access_token});
});

function buildCard(color, content) {
    var card = document.createElement("div");
    card.classList.add("card", color);
    card.textContent = content;
    return card;
}

var row = document.getElementsByClassName("cards")[0]; // TODO: there might be others
function fillRow(cards) {
    row.innerHTML = ""; // you ignoramus, do this right
    for (card of cards) {
        row.appendChild(buildCard("white", card));
    }
}
socket.on("cah_ping", function(data) {
    // Should we use bracket notation? Should we use camelCase because this is JavaScript? Should we delete this entire bloated bot and git commit seppuku? Maybe
    if (!data.joined) {
        document.getElementById("warning").textContent = "You're not in a game. Type !cah join in the group first.";
        return;
    }

    // Again... address this in a more effective way
    document.getElementsByClassName("black")[0].textContent = data.black_card;

    if (data.is_czar) {
        document.getElementById("czar").textContent = "You are Card Czar this round. Please select a card.";
        fillRow(data.selection);
    } else {
        // TODO: there's nothing stopping anyone from submitting their own cards on the server-side, just that they won't be shown.
        // You lazy idiot.
        document.getElementById("czar").textContent = "";
        fillRow(data.hand);
    }
});
