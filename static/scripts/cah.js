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

// Card list from which Czar chooses
var selection = document.getElementById("selection");
// Your own cards, from which you choose when not Czar
var hand = document.getElementById("hand");
function fillRow(row, cards) {
    // Empty whatever is in the row first
    while (row.firstChild) row.removeChild(row.firstChild);
    for (card of cards) {
        row.appendChild(buildCard("white", card));
    }
}
function fillSelection(cards, length) {
    if (!cards) cards = Array(length).fill("");
    fillRow(selection, cards);
}
function fillHand(cards) {
    fillRow(hand, cards);
}

socket.on("cah_ping", function(data) {
    console.log("Recieved ping from game server", data);

    document.getElementById("black").textContent = data.black_card;

    } else {
        // TODO: there's nothing stopping anyone from submitting their own cards on the server-side, just that they won't be shown.
        document.getElementById("czar").textContent = "";
        fillHand(data.hand);
    }
    fillSelection(data.selection, data.selection_length);
});
socket.on("cah_update_user", function(data) {
    console.log("Recieved user update from server", data);
    // If user hasn't joined a game, warn them.
    if (!data.joined) {
        document.getElementById("warning").textContent = "You're not in a game. Type !cah join in the group first.";
        document.getElementById("cah").style.display = "none";
        return;
    }

    document.getElementById("black").textContent = data.black_card;
    fillHand(data.hand);
    if (data.is_czar) {
        document.getElementById("czar").textContent = "You are Card Czar this round. Please select a card.";
        hand.style.opacity = 0.5;
    } else {
        // TODO: there's nothing stopping anyone from submitting their own cards on the server-side, just that they won't be shown.
        document.getElementById("czar").textContent = "";
        hand.style.opacity = 1;
    }
});

onclick = function(e) {
    if (e.target.classList.contains("card") && e.target.classList.contains("white")) {
        console.log("Clicked on a card.");
        var cardIndex = Array.prototype.indexOf.call(e.target.parentNode.children, e.target);
        // TEMPORARY for debugging
        is_czar =  (e.target.parentNode.id == "selection");

        var data = {
            "access_token": access_token,
            "card_index": cardIndex,
            // TEMPORARY
            "is_czar": is_czar,
        };
        socket.emit("cah_selection", data);
    }
};
