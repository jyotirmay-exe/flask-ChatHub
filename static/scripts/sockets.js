const sockio = io();
console.log(roomID);
const messageCont = document.querySelector(".message-container");

document.addEventListener("userSet", () => {
    if (roomID && usnm) {
        sockio.emit("client_join", { room: roomID, user: usnm });
    }
    else {
        console.error("roomID or usnm is not defined");
    }
});

function sendMessage(user, text) {
    sockio.emit("client_message", { user: user, text: text })
}

sockio.on("broadcast_join", (event) => {
    joinText = formatJoin(event.date, event.time, event.user);
    messageCont.innerHTML += `${joinText}`;
});

sockio.on("broadcast_message", (event) => {
    message = formatMessage(event.date, event.time, event.user, event.text);
    messageCont.innerHTML += message;
    document.getElementById("msg").value = "";
    scrollEnd();
    // console.log(`${event.user}: ${event.text}`);
});