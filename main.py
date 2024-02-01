from networktables import NetworkTables
from flask import Flask, request
from flask_socketio import SocketIO
from datetime import datetime
from random import random
import logging

logging.basicConfig(level=logging.DEBUG)

app = Flask(__name__)
socketio = SocketIO(app, cors_allowed_origins='*')

NetworkTables.initialize(server="10.96.11.2")

sd = NetworkTables.getTable("datatable")

from routes import *

def get_current_datetime():
    now = datetime.now()
    return now.strftime("%m/%d/%Y %H:%M:%S")    


def onUpdate(table, key, value, isNew):
    # print("valueChanged: key: '%s'; value: %s; isNew: %s" % (key, value, isNew))
    socketio.emit('updateData', {"kv": str(key) + "::" + str(value), "date": get_current_datetime()})


@socketio.on('connect')
def connect():
    global thread
    print('Client connected')

@socketio.on('disconnect')
def disconnect():
    print('Client disconnected',  request.sid)


def main():
    sd.addEntryListener(onUpdate)
    app.run()
    socketio.run(app, allow_unsafe_werkzeug=True)

if __name__ == "__main__":
    main() 
