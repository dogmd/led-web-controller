#!/usr/bin/env python3
# I really have no idea what I'm doing. This should be rewritten
import asyncio
import websockets
import json
import time
import ssl
import led_control.led_relay as leds

settings_file = 'led_control/settings.json'

async def communicate(websocket, path):
	try:
		while True:
			data_raw = await websocket.recv()
			data = json.loads(data_raw)
			if (data['changeStatus']):
				# The web interface has been changed, and led_control/settings.json needs to be updated
				print(f"Recieved new settings:\n{data_raw}")
				with open(settings_file, 'w') as settings:
					settings.write(data_raw)
				leds.update_settings()            
			else:
				# Otherwise, the web interface is requesting the current status
				with open(settings_file, 'r') as settings:
					status = settings.read()
				print('Sending status to web interface...', end='')
				await websocket.send(status)
				print('done')
	except websockets.exceptions.ConnectionClosed:
		print('connection to client closed')

ssl_context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
ssl_context.load_cert_chain('/etc/letsencrypt/live/pi.69craft.com/fullchain.pem', '/etc/letsencrypt/live/pi.69craft.com/privkey.pem')
web_interface = websockets.serve(communicate, '', 8888, ssl=ssl_context)

while True:
	try:
		asyncio.get_event_loop().run_until_complete(web_interface)
	except Exception:
		pass
	leds.main()
