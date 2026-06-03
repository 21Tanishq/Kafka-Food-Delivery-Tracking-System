from flask_socketio import SocketIO

socketio = SocketIO(cors_allowed_origins="*")

def emit_update(data):
    socketio.emit("update", data)