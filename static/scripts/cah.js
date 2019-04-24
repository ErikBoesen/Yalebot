onclick = function(e) {
    if (e.target.classList.contains("card")) {
        var cardIndex = Array.prototype.indexOf.call(e.target.parentNode.childNodes, e.target);

        var req = new XMLHttpRequest();
        req.open("POST", "");
        req.setRequestHeader("Content-Type", "application/json;charset=UTF-8");
        var url = new URL(url_string);
        ;
        req.send(JSON.stringify({
            "group_id": e.target.getAttribute("group_id"),
            // TODO: this is not a very elegant way to get the token.
            "access_token": url.searchParams.get("access_token"),
        }));
        req.onreadystatechange = function() {
            if (this.readyState == 4 && this.status == 200) {
                location.reload();
            }
        };
    }
}
