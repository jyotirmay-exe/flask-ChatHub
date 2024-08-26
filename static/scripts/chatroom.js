let usnm = "";

function formatMessage(date, time, user, text) 
{
    let message = `
        <div class="message">
            <span class="timestamp">${date}<br>${time}</span>
            <span class="username">[ ${user} ] :</span>
            <span class="text">${text}</span>
        </div>`;
    return message;
}

function formatJoin(date, time, user) 
{
    let message = `
        <div class="message">
            <span class="timestamp">${date}<br>${time}</span>
            <span class="username">[ ${user} ] :</span>
            <span class="text joinText">User connected. Welcome to the Room.</span>
        </div>`;
    return message;
}

function formatLeave(date, time, user) 
{
    let message = `
        <div class="message">
            <span class="timestamp">${date}<br>${time}</span>
            <span class="username">[ ${user} ] :</span>
            <span class="text leaveText">User disconnected. Goodbye.</span>
        </div>`;
    return message;
}

function sendHandler() 
{
    let text = document.getElementById("msg").value;
    if (text == null || text === "") 
    {
        return;
    }
    sendMessage(usnm, text);
}

function scrollEnd() 
{
    let currentScrollPosition = window.scrollY;
    let targetScrollPosition = document.body.scrollHeight;
    window.scrollTo({
        top: targetScrollPosition,
        behavior: 'smooth'
    });
}

function keyHandler(event) 
{
    if (event.key === "Enter") {
        sendHandler();
    }
}

window.onload = (event) => 
{
    while (true) {
        let userInput = prompt("Enter Display Name (No spaces. 12 characters max.):");
        if (userInput === null) {
            window.location.href = "/";
            break;
        }
        usnm = userInput.split(' ')[0].slice(0, 12);
        if (usnm !== "") {
            const userSetEvent = new Event('userSet');
            document.dispatchEvent(userSetEvent);
            break;
        }
    }
    scrollEnd();
};

function toggleMembers() 
{
    let userDiv = document.querySelector(".users-container");
    if (userDiv.hidden) {
        userDiv.hidden = false;
    } else {
        userDiv.hidden = true;
    }
}
