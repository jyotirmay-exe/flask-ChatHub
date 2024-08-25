let usnm = "";

function formatMessage(date, time, user, text) {
    date = date || new Date().toLocaleDateString();
    time = time || new Date().toLocaleTimeString("en-us", { hour12: false }).slice(0, 5);

    let message = `<div class="message">
                <span class="timestamp">${date}<br>${time}</span>
                <span class="username">${user}: </span>
                <span class="text">${text}</span>
                </div>`;
    return message;
}

function sendHandler() {
    text = document.getElementById("msg").value;
    if (text == null || text == "") { return; }
    message = formatMessage(null, null, usnm, text);
    const msgcont = document.querySelector('.message-container');
    msgcont.innerHTML += message;
    scrollEnd();
    document.getElementById("msg").value = "";
}

function scrollEnd() {
    window.scrollTo(0, document.body.scrollHeight);
}

function keyHandler(event) {
    if (event.key === "Enter") {
        sendHandler();
    }
}

document.addEventListener("DOMContentLoaded", (event) => {
    while (true) {
        usnm = prompt("Enter Display Name:");
        if (usnm == "") { continue; }
        else if (usnm == null) { window.location.href = "/"; break; }
        else {
            const event = new Event('userSet');
            document.dispatchEvent(event);
            break;
        }
    }

    scrollEnd();
});


function toggleMembers() {
    userDiv = document.querySelector(".users-container");
    if (userDiv.hidden) { userDiv.hidden = false; }
    else { userDiv.hidden = true; }
}