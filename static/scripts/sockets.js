const sockio = io({
    closeOnBeforeunload: false
});

const messageCont = document.querySelector(".message-container");

let tabHidden = false;

document.addEventListener("userSet", () => 
{
    if (roomID && usnm) 
    {
        sockio.emit("client_join", { room: roomID, user: usnm });
    } 
    else 
    {
        console.error("roomID or usnm is not defined");
    }
});

document.addEventListener("visibilitychange", () => 
{
    tabHidden = document.hidden;
    if (tabHidden) 
    {
        sockio.emit("client_leave", { room: roomID, user: usnm });
        console.log("Tab is now hidden.");
    } 
    else 
    {
        console.log("Tab is now visible.");
        sockio.emit("client_join", { room: roomID, user: usnm });
    }
});

function sendMessage(user, text) 
{
    sockio.emit("client_message", { room: roomID, user: user, text: text });
    console.log("Message sent:", text);
}

document.querySelector('.members-icon').addEventListener('click', () => {
    sockio.emit('client_getuserlist', { room: roomID, user: usnm });
});

sockio.on("broadcast_join", (event) => 
{
    const joinText = formatJoin(event.date, event.time, event.user);
    messageCont.innerHTML += `${joinText}`;
    scrollEnd();
    console.log("User joined:", event.user);
});

sockio.on("broadcast_leave", (event) => 
{
    const leaveText = formatLeave(event.date, event.time, event.user);
    messageCont.innerHTML += leaveText;
    scrollEnd();
    console.log("User left:", event.user);
});

sockio.on("broadcast_message", (event) => 
{
    const message = formatMessage(event.date, event.time, event.user, event.text);
    messageCont.innerHTML += message;
    document.getElementById("msg").value = "";
    scrollEnd();
    console.log("Received message from:", event.user, "Text:", event.text);
});

sockio.on("broadcast_userlist", (event) => 
{
    console.log(`Got User List : ${typeof(event.list)}`);
    ulist = document.querySelector(".users-list");
    ulist.innerHTML = "";
    event.list.forEach(ele => {
        ulist.innerHTML += `<li>${ele}</li>`;
    });
});

sockio.on("broadcast_room404", () => 
{
    alert("Room does not exist. Redirecting...");
    window.location.href="/";
});