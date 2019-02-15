#!/usr/bin/env python

# WS server example

import asyncio
import websockets
import json
import led-control.led_relay as controller

settings_file = 'led-control/settings.json'

async def communicate(websocket, path):
    while True:
        data_raw = await websocket.recv()
        data = json.loads(data_raw)
        if (data['changeStatus']):
            # The web interface has been changed, and led-control/settings.json needs to be updated
            print(f"Recieved new settings:\n{data_raw}")
            with open(settings_file, 'w') as settings:
                settings.write(data_raw)
			controller.update()
        else:
            # Otherwise, the web interface is requesting the current status
            with open(settings_file, 'r') as settings:
              status = settings.read()
            print('Sending status to web interface...', end='')
            await websocket.send(status)
            print('done')

controller.main()
start_server = websockets.serve(communicate, '', 8765)

asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()
