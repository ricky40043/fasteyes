import logging

from fastapi import FastAPI, Request, WebSocket

from app.Server.socket import sio
from app.api.routes.api import router as api_router
from app.db.database import engine, Base
from starlette.middleware.cors import CORSMiddleware

import socketio


Base.metadata.create_all(bind=engine)

origins = [
    "http://localhost:8080"
]


def create_app():
    app = FastAPI()
    # app.host = "localhost/127.0.0.1"
    # app.port = "8080"
    # app.servers ={"url": "https://localhost/127.0.0.1", "description": "Staging environment"}

    app.add_middleware(
        CORSMiddleware,
        allow_origins=origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"]
    )
    app.include_router(api_router)
    sio_app = socketio.ASGIApp(
        socketio_server=sio,
        other_asgi_app=app,
        socketio_path='/socket.io/'
    )
    app.add_route("/socket.io/", route=sio_app, methods=['GET', 'POST'])
    return app

# uvicorn app.main:app --host 192.168.45.63 --reload-dir app
