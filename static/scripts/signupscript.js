const queryString = window.location.search;
const urlParams = new URLSearchParams(queryString);

const username = urlParams.get('username');
const group = urlParams.get('group');

if (username != null) document.getElementById('username').value = username;
if (group != null) document.getElementById('group').value = group;