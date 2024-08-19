function showField() {
    ele00 = document.getElementById("createnew");
    ele01 = document.getElementById("joinexisting");
    ele1 = document.getElementById("roomID");
    ele2 = document.getElementById("join");
    ele00.style.display = "none";
    ele01.style.display = "none";
    ele1.style.display = "inline-block";
    ele2.style.display = "inline-block";
}

function editRoomID() {
    roomid = document.getElementById("roomID");
    roomid.value = roomid.value.toUpperCase();
    if(roomid.value.length>6) {
        roomid.value = roomid.value.slice(0,6);
    }
}

function redirectRoom() {
    roomid = document.getElementById("roomID").value;
    console.log(roomid);
    console.log("HERE");
    window.location.href=`/join_room/${roomid}`;
}