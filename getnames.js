var names = [];
var excluded = ['', 'Admin', 'Moderator', 'Rising Star'];
for (title of document.querySelectorAll('[ajaxify^="/groups/member_bio"]:not(._4bo_)')) {
	name = title.childNodes[0].textContent.split('\n')[0];
	if (excluded.indexOf(name) < 0) {
		names.push(name);
	}
}
document.body.textContent = JSON.stringify(names);
