onclick = function(e) {
    if (e.target.classList.contains("card")) {
        var cardIndex = Array.prototype.indexOf.call(e.target.parentNode.childNodes, e.target);

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
            } else {
                console.log("Failed to report data.", data);
            }
        };
    }
}
