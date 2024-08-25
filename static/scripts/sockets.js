const sockio = io({
    closeOnBeforeunload: false
  });

console.log(roomID);
const messageCont = document.querySelector(".message-container");
let tabHidden = false;

document.addEventListener("userSet", () => {
    if (roomID && usnm) {
        sockio.emit("client_join", { room: roomID, user: usnm });
    }
    else {
        console.error("roomID or usnm is not defined");
    }
});

document.addEventListener("visibilitychange", () => {
    tabHidden = document.hidden;
});

window.addEventListener("beforeunload", (event) => {
    if (!tabHidden) {
        sockio.emit("client_leave", { room: roomID, user: usnm });
    }
});

function sendMessage(user, text) {
    sockio.emit("client_message", { room: roomID, user: user, text: text });
}

sockio.on("broadcast_join", (event) => {
    const joinText = formatJoin(event.date, event.time, event.user);
    messageCont.innerHTML += `${joinText}`;
});

sockio.on("broadcast_leave", (event) => {
    const leaveText = formatLeave(event.date, event.time, event.user);
    messageCont.innerHTML += leaveText;
});

sockio.on("broadcast_message", (event) => {
    const message = formatMessage(event.date, event.time, event.user, event.text);
    messageCont.innerHTML += message;
    document.getElementById("msg").value = "";
    scrollEnd();
    // console.log(`${event.user}: ${event.text}`);
});
