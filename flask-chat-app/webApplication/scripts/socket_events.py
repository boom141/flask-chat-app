from flask_socketio import Namespace, send, emit, join_room, leave_room
from flask_login import current_user
from flask import request
import datetime

class global_chat(Namespace):
    def on_connect(self):
        print('[CLIENT CONNECTED]: ', request.sid)

    def on_disconnect(self):
        print('[CLIENT DISCONNECTED]: ', request.sid)

    def on_global_message(self, message):
        timestamp = datetime.datetime.now()
        data = [request.sid, current_user.username, message, f"{timestamp.strftime('%b %d, %Y %I:%M %p')}"]
        print(current_user.username, message, f"{timestamp.strftime('%b %d, %Y %I:%M %p')}")
        emit('global_message', data, broadcast=True)
