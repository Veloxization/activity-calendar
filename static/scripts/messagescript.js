var titleValid = False;
var messageValid = False;

const titleElement = document.getElementById("thread-name");
const messageElement = document.getElementById("message");
const submitButton = document.getElementById("submit-button");

function checkForm() {
    titleValid = checkTitle();
    messageValid = checkMessage();
    activateButton();
}

function checkTitle() {
    var title = titleElement.value;
    return title.length > 0 && title.length <= 256;
}

function checkMessage() {
    var message = messageElement.value;
    return message.length > 0 && message.length <= 5000;
}

function activateButton() {
    if (titleValid && messageValid) {
        submitButton.disabled = false;
    } else {
        submitButton.disabled = true;
    }
}