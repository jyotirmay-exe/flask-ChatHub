let usnm = "";

function formatMessage(date, time, user, text) {
    date = date || new Date().toLocaleDateString();
    time = time || new Date().toLocaleTimeString();

    let message = `<div class="message">
                <span class="timestamp">${date}<br>${time}</span>
                <span class="username">${user}: </span>
                <span class="text">${text}</span>
                </div>`;
    return message;
}

function sendHandler() {
    text = document.getElementById("msg").value;
    if(text==null || text=="") { return; }
    message = formatMessage(null,null,usnm,text);
    const msgcont = document.querySelector('.message-container');
    msgcont.innerHTML+=message;
    scrollEnd();
}

function scrollEnd() {
    window.scrollTo(0, document.body.scrollHeight);
}

function keyHandler(event) {
    if(event.key==="Enter") {
        sendHandler();
        document.getElementById("msg").value = "";
    }
}

document.addEventListener("DOMContentLoaded", () => {
    while(usnm=="" || usnm==null) {
        usnm = prompt("Enter Display Name:");
    }

    scrollEnd();
});
