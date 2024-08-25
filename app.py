from flask import Flask, render_template, redirect, url_for
from flask_socketio import SocketIO

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
        if hashed not in rooms and room_id not in rooms.values():
            rooms[hashed] = room_id
            logger.info(f"Created room: {room_id} ({hashed})")
            break

    return redirect(url_for("chatRoom", room_hash=hashed))

@app.route("/join_room/<room_id>")
def joinRoom(room_id):
    hashed = next((key for key in rooms if rooms[key] == room_id), None)
    if not hashed:
        logger.warning(f"Tried to join missing room: {room_id}")
        return render_template("not_found.html")
    
    logger.info(f"Joined room: {room_id} ({hashed})")
    return redirect(url_for("chatRoom", room_hash=hashed))

@app.route("/room/<room_hash>")
def chatRoom(room_hash):
    if room_hash not in rooms:
        logger.warning(f"Tried to access missing room: {room_hash}")
        return render_template("not_found.html")
    
    logger.info(f"Entered chat room: {room_hash} (ID: {rooms[room_hash]})")
    return render_template("chat_room.html", hashed=room_hash, room_id=rooms[room_hash])

@app.route("/")
def homepage():
    logger.info("Homepage accessed")
    return render_template('index.html')

# Socket Handling
@sockio.on("client_join")
def on_join(event):
    logger.info(f"User: \"{event['user']}\" joined Room ID: {event['room']}")
    sockio.emit("broadcast_join", {'date': getDate(), 'time': getTime(), 'user': event['user']})

@sockio.on("client_message")
def on_message(event):
    logger.info(f"Recvd. Message: {event['text']} from User: {event['user']}")
    sockio.emit("broadcast_message", {'date': getDate(), 'time': getTime(), 'user': event['user'], 'text': event['text']})

if __name__ == "__main__":
    sockio.run(app)