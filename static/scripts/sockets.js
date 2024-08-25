const sockio = io();
console.log(roomID);

document.addEventListener("userSet", () => {
    if (roomID && usnm) {
        sockio.emit("join", { room: roomID, user: usnm });
    }
    else {
        console.error("roomID or usnm is not defined");
    }
});