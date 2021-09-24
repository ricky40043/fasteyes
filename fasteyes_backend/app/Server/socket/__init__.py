import json
from collections import OrderedDict

import jsonify as jsonify
import socketio

background_task_started = False

sio = socketio.AsyncServer(
    async_mode='asgi',
    cors_allowed_origins=[])  # logger=False)

# sio = socketio.AsyncServer(
#     async_mode='asgi')  # logger=False)

Data = None
Title = None


def send_data(title, data):
    global Data
    global Title
    Data = data
    Title = title


async def background_task():
    # Example of how to send server generated events to clients.
    count = 0
    while True:
        global Data
        global Title
        await sio.sleep(1)

        # count += 1
        # await sio.emit('Server', {'data': "Hello, Client",
        #                           'count': count})
        if Data:
            print("SocketIO In")
            # app_json = json.dumps(Data)

            await sio.emit(Title, Data)

            Data = None
            Title = None


@sio.event
async def connect(sid, environ):
    print(f'{sid} connected!')
    global background_task_started
    if not background_task_started:
        sio.start_background_task(background_task)
        background_task_started = True
    await sio.emit("Server", {'data': "Connect",
                              'count': 0})


@sio.event
async def disconnect(sid):
    print('disconnect', sid)
