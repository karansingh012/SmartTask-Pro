from flask import Flask
from flask_socketio import SocketIO


def register_socketio_handlers(socketio: SocketIO, app: Flask) -> None:
    @socketio.on("connect")
    def handle_connect():
        app.logger.info("SocketIO client connected")

    @socketio.on("disconnect")
    def handle_disconnect():
        app.logger.info("SocketIO client disconnected")
