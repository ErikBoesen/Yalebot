// Retrieve access token from URL parameter
var access_token = (new URL(location.href)).searchParams.get("access_token");

// Initiate connection to websocket, and listen for connection
var socket = io.connect(location.protocol + "//" + location.host);
socket.on("connect", function() {
    console.log(socket.connected ? "Connected" : "Disconnected", socket);
    socket.emit("cah_connect", {"access_token": access_token});
});

// Create card elements easily
function buildCard(color, content) {
    var card = document.createElement("div");
    card.classList.add(color, "card");
    card.textContent = content;
    return card;
}

var elem = {
    // Disconnection warning
    warning: document.getElementById("warning"),
    // Parent element holding all game components
    game: document.getElementById("game"),
    // Line saying that you're currently Czar
    czar: document.getElementById("czar"),
    // Black card
    black: document.getElementById("black"),
    // Card list from which Czar chooses
    selection: document.getElementById("selection"),
    // Your own cards, from which you choose when not Czar
    hand: document.getElementById("hand"),
}
function fillRow(row, cards) {
    // Empty whatever is in the row first
    while (row.firstChild) row.removeChild(row.firstChild);
    for (card of cards) {
        row.appendChild(buildCard("white", card));
    }
}
function fillSelection(cards, length) {
    if (!cards) cards = Array(length).fill("");
    fillRow(elem.selection, cards);
}
function fillHand(cards) {
    fillRow(elem.hand, cards);
}

socket.on("cah_ping", function(data) {
    console.log("Received ping from game server", data);
    elem.black.textContent = data.black_card;
    fillSelection(data.selection, data.selection_length);
});
socket.on("cah_update_user", function(data) {
    console.log("Received user update from server", data);
    if (data.joined) {
        elem.game.style.display = "block";
        fillHand(data.hand);
        if (data.is_czar) {
            elem.czar.textContent = "You are Card Czar this round. Please select a card.";
            elem.hand.classList.add("disabled");
        } else {
            elem.czar.textContent = "";
            elem.hand.classList.remove("disabled");
        }
    } else {
        // If user hasn't joined a game, warn them.
        elem.warning.textContent = "You're not in a game. Type !cah join in the group first.";
        elem.game.style.display = "none";
    }
});

onclick = function(e) {
    if (
        e.target.classList.contains("card", "white") &&
        !(e.target.parentNode.classList.contains("disabled"))
    ) {
        console.log("Clicked on a card.");
        var cardIndex = Array.prototype.indexOf.call(e.target.parentNode.children, e.target);

        var data = {
            "access_token": access_token,
            "card_index": cardIndex,
        };
        socket.emit("cah_selection", data);
        elem.hand.classList.add("disabled");
    }
};
