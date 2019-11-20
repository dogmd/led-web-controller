#!/usr/bin/python3
from flask import Flask, request, jsonify
import json
import multiprocessing
import led_relay

app = Flask(__name__)

# Run the led_relay main loop and listen for settings updates
def led_interface(queue):
    while True:
        command = ''
        if (not queue.empty()):
            command = queue.get()
        if (command == 'update'):
            led_relay.update_settings()
        elif (command == 'stop'):
            break
        led_relay.main()

# Start the led worker child process
queue = multiprocessing.Queue()
leds = multiprocessing.Process(target=led_interface, args=(queue,))
leds.start()

@app.route('/settings', methods=['GET'])
def get_settings():
	with open('settings.json', 'r') as settings:
		return settings.read(), 200

@app.route('/settings', methods=['PUT', 'POST'])
def set_settings():
    # This way ensures that data is valid json
    new_settings = json.dumps(request.get_json(force=True))
    with open('settings.json', 'w') as settings:
        settings.write(new_settings)
    # Tell the led worker to update its settings
    queue.put('update')
    effects = map(lambda e: e[0].__name__, led_relay.effect_controller.effects)
    effects = { 'enabled_effects': list(effects) }
    return jsonify(effects), 200
    

if __name__ == '__main__':
    app.run(debug=True)

    queue.close()
    queue.join_thread()
    leds.join()
