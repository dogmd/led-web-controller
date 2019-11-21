#!/usr/bin/python3
from flask import *
import json
import multiprocessing
import led_relay
import effect_controller
import time

app = Flask(__name__)

<<<<<<< HEAD
=======
def millis_time():
    return int(round(time.time() * 1000))

>>>>>>> 2ac747b651dce22b29b2f3ad9270ca3d817bf632
# Run the led_relay main loop and listen for commands
def led_interface(commands, replies):
    print('LED worker started')
    last_alert = millis_time()
    start = millis_time()
    desired_tps = 1 / effect_controller.DELAY
    last_ticks = 0
    while True:
        command = ''
        if (not commands.empty()):
            command = commands.get()
        if (command == 'update'):
            led_relay.update_settings()
            enabled_effects = map(lambda e: e[0].__name__, led_relay.effect_controller.enabled_effects)
            enabled_effects = { 'enabled_effects': list(enabled_effects) }
            replies.put(enabled_effects)
        elif (command == 'stop'):
            break
        
        if (millis_time() - last_alert >= 1000):
            actual_tps = led_relay.effect_controller.time - last_ticks
            last_alert = millis_time()
            last_ticks = led_relay.effect_controller.time
            if (actual_tps < desired_tps * 0.95):
                print('Running behind! Desired TPS: {}, Actual TPS: {}'.format(desired_tps, actual_tps))
            else:
                print('Desired TPS: {}, Actual TPS: {}'.format(desired_tps, actual_tps))

        led_relay.main()


@app.route('/settings/<effect_name>', methods=['GET'])
def get_settings(effect_name):
    if (effect_name == 'all'):
        with open('settings.json', 'r') as settings:
            data = settings.read()
        return Response(response=data, status=200, mimetype='application/json')
    else:
        return jsonify(led_relay.effect_controller.settings['effects'][effect_name]), 200
        

@app.route('/settings', methods=['PUT', 'POST'])
def set_settings():
    # This way ensures that data is valid json
    new_settings = json.dumps(request.get_json(force=True))
    with open('settings.json', 'w') as settings:
        settings.write(new_settings)
    # Tell the led worker to update its settings
    commands.put('update')
    enabled_effects = replies.get()
    # Get currently enabled effects
    return jsonify(enabled_effects), 200    


if __name__ == '__main__':
    # Start the led worker child process
    commands = multiprocessing.Queue()
    replies = multiprocessing.Queue()
    leds = multiprocessing.Process(target=led_interface, args=(commands, replies))
    leds.start()
    # Start Flask
    app.run(debug=True, use_reloader=False, host='192.168.8.155', port='5000')

    commands.close()
    commands.join_thread()
    replies.close()
    replies.join_thread()
    leds.join()
