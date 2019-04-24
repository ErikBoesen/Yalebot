onclick = function(e) {
    if (e.target.classList.contains("card")) {
        var cardIndex = Array.prototype.indexOf.call(e.target.parentNode.childNodes, e.target);
    }
}
