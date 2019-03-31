onclick = function(e) {
    if (e.target.tagName == 'BUTTON' && e.target.classList.contains('delete')) {
        if (confirm('Really delete bot?')) {
            var req = new XMLHttpRequest();
            req.open('POST', '/delete');
            req.setRequestHeader('Content-Type', 'application/json;charset=UTF-8');
            req.send(JSON.stringify({
                'group_id': e.target.getAttribute('group_id'),
                // TODO: this is not a very elegant way to get the token.
                'access_token': document.getElementsByName('access_token')[0].value,
            }));
            req.onreadystatechange = function() {
                if (this.readyState == 4 && this.status == 200) {
                    location.reload();
                }
            };
        }
    }
}
