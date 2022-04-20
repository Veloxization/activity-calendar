const queryString = window.location.search;
const urlParams = new URLSearchParams(queryString);

const username = urlParams.get('username');

if (username != null) document.getElementById('username').value = username;