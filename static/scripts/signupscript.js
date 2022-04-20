const queryString = window.location.search;
const urlParams = new URLSearchParams(queryString);

const username = urlParams.get('username');
const group = urlParams.get('group');

if (username != null) document.getElementById('username').value = username;
if (group != null) document.getElementById('group').value = group;

var usernameValid = false;
var passwordValid = false;
var passwordsMatch = false;

const usernameField = document.getElementById('username');
const passwordField = document.getElementById('password');
const passwordAgainField = document.getElementById('password-again');
const submitButton = document.getElementById('submit-button');
const usernameError = document.getElementById('username-error');
const passwordError = document.getElementById('password-error');
const passwordAgainError = document.getElementById('password-again-error');

const re = /^[a-zA-Z0-9]+$/;

function checkForm() {
    usernameValid = checkUsername();
    passwordValid = checkPassword();
    passwordsMatch = checkPasswordMatch();
    activateButton();
}

function checkUsername() {
    var username = usernameField.value;
    if (!re.test(username)) {
        usernameValid = false;
        usernameError.innerHTML = "Invalid characters in username!";
        return false;
    }
    if (username.length < 3) {
        usernameValid = false;
        usernameError.innerHTML = "Username too short!";
        return false;
    }
    if (username.length > 20) {
        usernameValid = false;
        usernameError.innerHTML = "Username too long!";
        return false;
    }
    usernameError.innerHTML = "";
    return true;
}

function checkPassword() {
    var password = passwordField.value
    if (password === '') {
        passwordValid = false;
        passwordError.innerHTML = "";
        return false;
    }
    if (password.includes(' ')) {
        passwordValid = false;
        passwordError.innerHTML = "Password contains spaces!";
        return false;
    }
    if (password.length < 8) {
        passwordValid = false;
        passwordError.innerHTML = "Password too short!";
        return false;
    }
    if (password.length > 64) {
        passwordValid = false;
        passwordError.innerHTML = "Password too long!";
        return false;
    }
    passwordError.innerHTML = "";
    return true;
}

function checkPasswordMatch() {
    var password = passwordField.value;
    var passwordAgain = passwordAgainField.value;
    if (password != passwordAgain) {
        passwordsMatch = false;
        passwordAgainError.innerHTML = "Not matching!";
        return false;
    }
    passwordAgainError.innerHTML = "";
    return true;
}

function activateButton() {
    if (usernameValid && passwordValid && passwordsMatch) {
        submitButton.disabled = false;
    } else {
        submitButton.disabled = true;
    }
}