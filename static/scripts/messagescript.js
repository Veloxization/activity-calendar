var titleValid = false;
var messageValid = false;
var recipientValid = false;

const titleElement = document.getElementById("thread-name");
const messageElement = document.getElementById("message");
const recipientElement = document.getElementById("recipient");
const submitButton = document.getElementById("submit-button");

function checkForm() {
    titleValid = checkTitle();
    messageValid = checkMessage();
    recipientValid = checkRecipient();
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

function checkRecipient() {
    var recipient = recipientElement.value;
    console.log(recipient);
    return recipient.length > 0;
}

function activateButton() {
    if (titleValid && messageValid && recipientValid) {
        submitButton.disabled = false;
    } else {
        submitButton.disabled = true;
    }
}