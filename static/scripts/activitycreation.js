const queryString = window.location.search;
const urlParams = new URLSearchParams(queryString);

const activity = urlParams.get('activity');

if (activity != null) document.getElementById('activity-name').value = activity;