document.getElementById('accept').onclick = function() {
    document.getElementById('add').disabled = !this.checked;
}

onclick = function(e) {
    if (e.target.tagName == 'BUTTON' && e.target.classList.contains('delete')) {
        if (confirm('Really delete bot?')) {
            var req = new XMLHttpRequest();
            req.open('/delete/
        }
    }
}
