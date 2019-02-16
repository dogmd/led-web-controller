#!/usr/bin/env python
import asyncio
import websockets
import json

settings_file = 'led_control/settings.json'
needs_update = False

async def communicate(websocket, path):
    while True:
        data_raw = await websocket.recv()
        data = json.loads(data_raw)
        if (data['changeStatus']):
            # The web interface has been changed, and led_control/settings.json needs to be updated
            print(f"Recieved new settings:\n{data_raw}")
            with open(settings_file, 'w') as settings:
                settings.write(data_raw)
            needs_update = True
        else:
            # Otherwise, the web interface is requesting the current status
            with open(settings_file, 'r') as settings:
              status = settings.read()
            print('Sending status to web interface...', end='')
            await websocket.send(status)
            print('done')

web_interface = websockets.serve(communicate, '', 8765)

asyncio.get_event_loop().run_until_complete(web_interface)
asyncio.get_event_loop().run_forever()
