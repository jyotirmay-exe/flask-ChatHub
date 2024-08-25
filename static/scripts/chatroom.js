let usnm = "";

function formatMessage(date, time, user, text) {
    let message = `<div class="message">
                <span class="timestamp">${date}<br>${time}</span>
                <span class="username">[ ${user} ] : </span>
                <span class="text">${text}</span>
                </div>`;
    return message;
}

function formatJoin(date, time, user) {
    let message = `<div class="message">
                <span class="timestamp">${date}<br>${time}</span>
                <span class="username">[ ${user} ] : </span>
                <span class="text joinText">User connected. Welcome to the Room.</span> 
                </div>`;
    return message;
}

function formatLeave(date, time, user) {
    let message = `<div class="message">
                <span class="timestamp">${date}<br>${time}</span>
                <span class="username">[ ${user} ] : </span>
                <span class="text leaveText">User disconnected. Goodbye.</span> 
                </div>`;
    return message;
}

function sendHandler() {
    text = document.getElementById("msg").value;
    if (text == null || text == "") { return; }
    sendMessage(usnm, text);
}

function scrollEnd() {
    window.scrollTo(0, document.body.scrollHeight);
}

function keyHandler(event) {
    if (event.key === "Enter") {
        sendHandler();
    }
}

window.onload = (event) => {
    while (true) {
        usnm = prompt("Enter Display Name (No spaces. 12 characters max.):").split(' ')[0].slice(0, 12);
        if (usnm == "") { continue; }
        else if (usnm == null) { window.location.href = "/"; break; }
        else {
            const event = new Event('userSet');
            document.dispatchEvent(event);
            break;
        }
    }

    scrollEnd();
};


function toggleMembers() {
    userDiv = document.querySelector(".users-container");
    if (userDiv.hidden) { userDiv.hidden = false; }
    else { userDiv.hidden = true; }
}