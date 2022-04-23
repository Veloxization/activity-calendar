const queryString = window.location.search;
const urlParams = new URLSearchParams(queryString);

const username = urlParams.get('username');
const usernameField = document.getElementById('username');
const passwordField = document.getElementById('password');
const submitButton = document.getElementById('submit-button');

var usernameValid = false;
var passwordValid = false;

if (username != null) document.getElementById('username').value = username;

function checkForm() {
    usernameValid = checkUsername();
    passwordValid = checkPassword();
    activateButton();
}

function checkUsername() {
    var username = usernameField.value;
    return username.length >= 3 && username.length <= 20;
}

function checkPassword() {
    var password = passwordField.value;
    return password.length >= 8 && password.length <= 64
}

function activateButton() {
    if (usernameValid && passwordValid) {
        submitButton.disabled = false;
    } else {
        submitButton.disabled = true;
    }
}