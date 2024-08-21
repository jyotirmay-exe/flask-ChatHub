function sendHandler() {
    console.log(document.getElementById("msg").value);
}

function keyHandler(event) {
    if(event.key==="Enter") {
        sendHandler();
        document.getElementById("msg").value = "";
    }
}

document.addEventListener("DOMContentLoaded", () => {
    const msgcont = document.querySelector('.message-container');
    content = msgcont.innerHTML;

    for (let i = 0; i < 50; i++) {
        msgcont.innerHTML+=content;
    }

    window.scrollTo(0, document.body.scrollHeight);
});
