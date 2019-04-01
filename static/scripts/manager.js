onclick = function(e) {
    if (e.target.tagName == 'BUTTON' && e.target.classList.contains('delete')) {
        if (confirm('Really delete bot?')) {
            var req = new XMLHttpRequest();
            req.open('POST', '/delete');
            req.setRequestHeader('Content-Type', 'application/json;charset=UTF-8');
            console.log({
                'group_id': e.target.getAttribute('group_id'),
                // TODO: this is not a very elegant way to get the token.
                'access_token': document.getElementById('access_token').value,
            });
            req.send(JSON.stringify({
                'group_id': e.target.getAttribute('group_id'),
                // TODO: this is not a very elegant way to get the token.
                'access_token': document.getElementById('access_token').value,
            }));
            req.onreadystatechange = function() {
                if (this.readyState == 4 && this.status == 200) {
                    location.reload();
                }
            };
        }
    }
}

var avatarURLInput = document.getElementsByName('avatar_url')[0],
    avatarPreview = document.getElementById('avatar_preview');
function previewAvatar() {
    avatarPreview.style.backgroundImage = 'url(' + avatarURLInput.value + ')';
}
previewAvatar();
avatarURLInput.oninput = previewAvatar;
