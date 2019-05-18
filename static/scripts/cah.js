var access_token = (new URL(location.href)).searchParams.get("access_token");

var socket = io.connect(location.protocol + "//" + location.host);
socket.on("connect", function(data) {
    console.log(data.connected ? "Connected" : "Disconnected", data);
    socket.emit("cah_connect", {"access_token": access_token});
});

function buildCard(color, content) {
    var card = document.createElement("div");
    card.classList.add("card", color);
    card.textContent = content;
    return card;
}

var selection = document.getElementById("selection"); // TODO: there might be others
var hand = document.getElementById("hand");
function fillRow(row, cards) {
    row.innerHTML = ""; // you ignoramus, do this right
    for (card of cards) {
        row.appendChild(buildCard("white", card));
    }
}
function fillSelection(cards) {
    fillRow(selection, cards);
}
function fillHand(cards) {
    fillRow(hand, cards);
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
        fillSelection(data.selection);
        // THIS IS ALL TEMPORARY FOR TESTING AND WILL ALLOW A CZAR TO SUBMIT CARDS WHICH THEY SHOULDN'T BE ABLE TO
        fillHand(data.hand);
    } else {
        // TODO: there's nothing stopping anyone from submitting their own cards on the server-side, just that they won't be shown.
        // You lazy idiot.
        document.getElementById("czar").textContent = "";
        fillHand(data.hand);
    }
});

onclick = function(e) {
    if (e.target.classList.contains("card") && e.target.classList.contains("white")) {
        console.log("Clicked on a card.");
        var cardIndex = Array.prototype.indexOf.call(e.target.parentNode.children, e.target);
        // TEMPORARY for debugging
        is_czar =  (e.target.parentNode.id == "selection");

        var url = new URL(location.href);
        var data = {
            "access_token": url.searchParams.get("access_token"),
            "card_index": cardIndex,
            "is_czar": is_czar,
        };
        socket.emit("cah_selection", data);
    }
};
