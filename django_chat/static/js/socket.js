const socket = new WebSocket(`ws://localhost/ws/chat/`);
const messagesSection = document.getElementById('messages')

let messagesExists = messagesSection.innerHTML.length;

socket.onmessage = function(event) {
    fromServer = JSON.parse(event.data);
    fromServerData = fromServer['payload'];

    onNewMessage();

    console.log(fromServerData);

    if (fromServer["type"] == "create") {
        messageHTML = getNewMessageHTML(
            message_id=fromServerData['message_id'],
            username=fromServerData['username'],
            text=fromServerData['message']
        );
        messagesSection.innerHTML += messageHTML;
    } else if (fromServer["type"] == "delete") {
        document.getElementById(fromServerData["message_id"]).style.display = "none";
    }
};

function sendMessage(event) {
    socket.send(JSON.stringify({
        type: 'create',
        payload: {
            userid: '{{ user.id }}',
            username: '{{ user.username }}',
            message: getMessageText()
        }
    }));
}

function deleteMessage(message_id) {
    socket.send(JSON.stringify({
        type: 'delete',
        payload: {
            message_id: message_id,
        }
    }));
}

function onNewMessage() {
    messagesExists = true;
    document.getElementById('message-input').value = '';
}

function addMessage() {
    messageHTML = getNewMessageHTML(
        message_id=fromServerData['message_id'],
        username=fromServerData['username'],
        text=fromServerData['message']
    );
    messagesSection.innerHTML += messageHTML;
}

function getNewMessageHTML(message_id, username, text) {
    return `
    <div id=${message_id} class="message-text">
    <img src="https://cdn-icons-png.flaticon.com/512/151/151882.png" class="field-arrow field-arrow-static field-arrow-X" onclick="deleteMessage(${ message_id });">
    ${username}
    <img src="https://cdn-icons-png.flaticon.com/512/271/271226.png" class="field-arrow field-arrow-static"> ${text} </div>
    `
}

function getMessageText() {
    return document.getElementById('message-input').value
}
