from networktables import NetworkTables
from flask import Flask, render_template, request
from flask_socketio import SocketIO
from threading import Lock
from datetime import datetime
from random import random
thread = None
thread_lock = Lock()

app = Flask(__name__)
socketio = SocketIO(app, cors_allowed_origins='*')


def get_current_datetime():
    now = datetime.now()
    return now.strftime("%m/%d/%Y %H:%M:%S")    

def main():
    NetworkTables.initialize(server="10.96.11.2")
    print(NetworkTables._tables)

    app.run()
    socketio.run(app)

# home
@app.route("/")
def home():
    return render_template('index.html')

def background_thread():
    print("Updating data")
    while True:
        socketio.emit('updateData', {'value': (NetworkTables.getTable("SmartDashboard").getNumber("Motor-Shooter Esquerdo",0) * 100), "date": get_current_datetime()})
        socketio.sleep(1)

@socketio.on('connect')
def connect():
    global thread
    print('Client connected')

    global thread
    with thread_lock:
        if thread is None:
            thread = socketio.start_background_task(background_thread)

@socketio.on('disconnect')
def disconnect():
    print('Client disconnected',  request.sid)

if __name__ == "__main__":
    main() 
