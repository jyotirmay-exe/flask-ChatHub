from flask import Flask, render_template, redirect, url_for
from flask_socketio import SocketIO, join_room, leave_room

from modules.utils import *
from modules.logger import *

app = Flask(__name__)

sockio = SocketIO(app)
logger = getLogger()

rooms = {}

@app.route("/create_room")
def newRoom():
    while True:
        room_id = generate_room_id()
        hashed = hasher(room_id)
        room_id_exists = room_id in rooms.values()
        hashed_exists = hashed in rooms
        if not hashed_exists and not room_id_exists:
            rooms[hashed] = room_id
            logger.info(f"Created room: {room_id} ({hashed})")
            break

    return redirect(url_for("chatRoom", room_hash=hashed))

@app.route("/join_room/<room_id>")
def joinRoom(room_id):
    hashed = None
    for key in rooms:
        if rooms[key] == room_id:
            hashed = key
            break

    if hashed is None:
        logger.warning(f"Tried to join missing room: {room_id}")
        return render_template("not_found.html")
    
    logger.info(f"Joined room: {room_id} ({hashed})")
    return redirect(url_for("chatRoom", room_hash=hashed))

@app.route("/room/<room_hash>")
def chatRoom(room_hash):
    if room_hash not in rooms:
        logger.warning(f"Tried to access missing room: {room_hash}")
        return render_template("not_found.html")
    
    room_id = rooms[room_hash]
    logger.info(f"Entered chat room: {room_hash} (ID: {room_id})")
    return render_template("chat_room.html", hashed=room_hash, room_id=room_id)

@app.route("/")
def homepage():
    logger.info("Homepage accessed")
    return render_template('index.html')

# Socket Handling
@sockio.on("client_join")
def on_join(data):
    room = data['room']
    user = data['user']
    join_room(room)
    log_message = f"User: \"{user}\" joined Room ID: {room}"
    logger.info(log_message)
    
    broadcast_data = {
        'date': getDate(),
        'time': getTime(),
        'user': user
    }
    sockio.emit("broadcast_join", broadcast_data, room=room)

@sockio.on("client_leave")
def on_leave(data):
    room = data['room']
    user = data['user']
    leave_room(room)
    log_message = f"User: \"{user}\" left Room ID: {room}"
    logger.info(log_message)
    
    broadcast_data = {
        'date': getDate(),
        'time': getTime(),
        'user': user
    }
    sockio.emit("broadcast_leave", broadcast_data, room=room)

@sockio.on("client_message")
def on_message(data):
    room = data['room']
    user = data['user']
    text = data['text']
    log_message = f"Recvd. Message: {text} from User: {user} in Room: {room}"
    logger.info(log_message)
    
    broadcast_data = {
        'date': getDate(),
        'time': getTime(),
        'user': user,
        'text': text
    }
    sockio.emit("broadcast_message", broadcast_data, room=room)

if __name__ == "__main__":
    sockio.run(app)
