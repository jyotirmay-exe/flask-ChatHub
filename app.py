from flask import Flask, render_template, redirect, url_for

from modules.utils import *

app = Flask(__name__)

rooms = {}

@app.route("/create_room")
def newRoom():
    while True:
        room_id = generate_room_id()
        hashed = hasher(room_id)
        if hashed not in rooms and room_id not in rooms.values():
            rooms[hashed] = room_id
            break

    return f"NEW ROOM HERE - {room_id} - {hashed}"

@app.route("/join_room/<room_id>")
def joinRoom(room_id):
    hashed = next((key for key in rooms if rooms[key] == room_id), None)
    if not hashed:
        return render_template("not_found.html")
    app.logger.info(f"EXISTING ROOM HERE - {room_id} - {hashed}")
    return redirect(url_for("chatRoom",room_hash=hashed))

@app.route("/room/<room_hash>")
def chatRoom(room_hash):
    app.logger.info(f"This is the existing chat room - {room_hash}")

@app.route("/")
def homepage():
    return render_template('index.html')

if __name__=="__main__":
    app.run()