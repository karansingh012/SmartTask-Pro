from flask_socketio import SocketIO

from .events import register_socketio_handlers


socketio = SocketIO(cors_allowed_origins="*")


def init_socketio(app):
    socketio.init_app(app)
    register_socketio_handlers(socketio, app)
