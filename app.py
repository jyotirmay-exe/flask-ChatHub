from flask import Flask, render_template, redirect, url_for
from flask_socketio import SocketIO, join_room, leave_room
import threading
import time

from modules.utils import *
from modules.logger import *

app = Flask(__name__)

sockio = SocketIO(app)
logger = getLogger()

rooms = {}
users = {'room':[]}

pending_deletion = {}

def delayedDelete(room, delay=60):
    log_message = f"Initiating delayed deletion for Room: {room} with delay: {delay}s"
    logger.info(log_message)
    
    threading.Timer(delay, delete_room, args=[room]).start()
    log_message = f"Room: {room} queued for deletion after {delay}s"
    logger.info(log_message)

def delete_room(room):
    hashed = getHash(room)
    
    if len(users.get(room, [])) == 0:
        log_message = f"No users found in Room: {room}, proceeding with deletion."
        logger.info(log_message)
        
        if room in pending_deletion:
            del rooms[hashed]
            del users[room]
            del pending_deletion[room]
            log_message = f"Deleted Vacant Room ID: {room} ({hashed})"
            logger.info(log_message)
        else:
            log_message = f"Room: {room} was not found in pending_deletion. Skipping deletion."
            logger.warning(log_message)
    else:
        log_message = f"Room: {room} still has users, canceling deletion."
        logger.warning(log_message)

def getHash(roomID):
    for room in rooms:
        if rooms[room] == roomID:
            log_message = f"Found hash for Room ID: {roomID}, Hash: {room}"
            logger.info(log_message)
            return room
    
    log_message = f"No hash found for Room ID: {roomID}"
    logger.warning(log_message)
    return None

@app.route("/create_room")
def newRoom():
    log_message = "Creating a new room..."
    logger.info(log_message)
    
    while True:
        room_id = generate_room_id()
        hashed = hasher(room_id)
        room_id_exists = room_id in rooms.values()
        hashed_exists = hashed in rooms
        
        if not hashed_exists and not room_id_exists:
            rooms[hashed] = room_id
            users[room_id] = []
            logger.info(f"Created room: {room_id} ({hashed})")
            break
        else:
            logger.warning(f"Room ID: {room_id} or Hash: {hashed} already exists. Generating new ID.")
    
    return redirect(url_for("chatRoom", room_hash=hashed))

@app.route("/join_room/<room_id>")
def joinRoom(room_id):
    log_message = f"Attempting to join Room ID: {room_id}"
    logger.info(log_message)
    
    hashed = None
    for key in rooms:
        if rooms[key] == room_id:
            hashed = key
            break
    
    if hashed is None:
        logger.warning(f"Room ID: {room_id} does not exist.")
        return render_template("not_found.html")
    
    logger.info(f"Successfully joined Room: {room_id} ({hashed})")
    return redirect(url_for("chatRoom", room_hash=hashed))

@app.route("/room/<room_hash>")
def chatRoom(room_hash):
    log_message = f"Accessing Chat Room with Hash: {room_hash}"
    logger.info(log_message)
    
    if room_hash not in rooms:
        logger.warning(f"Room Hash: {room_hash} does not exist.")
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
    log_message = f"User: {user} is attempting to join Room: {room}"
    logger.info(log_message)
    
    join_room(room)
    
    if room in pending_deletion:
        pending_deletion[room].do_run = False
        del pending_deletion[room]
        log_message = f"Removed Room: {room} from deletion queue"
        logger.info(log_message)
    
    try:
        users[room].append(user)
        log_message = f"User: \"{user}\" successfully joined Room ID: {room}"
        logger.info(log_message)
    except KeyError:
        sockio.emit("broadcast_room404", room=room)
        log_message = f"Error: Room ID: {room} not found in users. Emitting Room 404."
        logger.error(log_message)
        return
    
    broadcast_data = {
        'date': getDate(),
        'time': getTime(),
        'user': user
    }
    sockio.emit("broadcast_join", broadcast_data, room=room)
    
    userlist = users[room]
    broadcast_data = {
        'date': getDate(),
        'time': getTime(),
        'list': userlist
    }
    
    sockio.emit("broadcast_userlist", broadcast_data, room=room)

@sockio.on("client_leave")
def on_leave(data):
    room = data['room']
    user = data['user']
    log_message = f"User: {user} is attempting to leave Room: {room}"
    logger.info(log_message)
    
    leave_room(room)
    
    try:
        users[room].remove(user)
        log_message = f"User: \"{user}\" successfully left Room ID: {room}"
        logger.info(log_message)
    except KeyError:
        sockio.emit("broadcast_room404", room=room)
        log_message = f"Error: Room ID: {room} not found in users. Emitting Room 404."
        logger.error(log_message)
        return
    
    broadcast_data = {
        'date': getDate(),
        'time': getTime(),
        'user': user
    }
    sockio.emit("broadcast_leave", broadcast_data, room=room)
    
    if len(users[room]) == 0:
        log_message = f"Room ID: {room} is now empty. Initiating delayed deletion."
        logger.info(log_message)
        deletion_thread = threading.Thread(target=delayedDelete, args=(room,))
        pending_deletion[room] = deletion_thread
        deletion_thread.start()
        return
    
    userlist = users[room]
    broadcast_data = {
        'date': getDate(),
        'time': getTime(),
        'list': userlist
    }
    
    sockio.emit("broadcast_userlist", broadcast_data, room=room)

@sockio.on("client_message")
def on_message(data):
    room = data['room']
    user = data['user']
    text = data['text']
    log_message = f"Received Message: {text} from User: {user} in Room: {room}"
    logger.info(log_message)
    
    if not text:
        log_message = f"Warning: Empty message received from User: {user} in Room: {room}"
        logger.warning(log_message)
    
    broadcast_data = {
        'date': getDate(),
        'time': getTime(),
        'user': user,
        'text': text
    }
    sockio.emit("broadcast_message", broadcast_data, room=room)

@sockio.on("client_getuserlist")
def on_getuserlist(data):
    room = data['room']
    user = data['user']
    log_message = f"User: {user} requested user list for Room ID: {room}"
    logger.info(log_message)
    
    userlist = users.get(room, [])
    if not userlist:
        log_message = f"Warning: No users found in Room ID: {room}."
        logger.warning(log_message)
    
    broadcast_data = {
        'date': getDate(),
        'time': getTime(),
        'list': userlist
    }
    
    sockio.emit("broadcast_userlist", broadcast_data, room=room)

if __name__ == "__main__":
    log_message = "Starting Flask-SocketIO application..."
    logger.info(log_message)
    
    sockio.run(app)
