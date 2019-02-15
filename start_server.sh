/usr/bin/tmux kill-session -t websocket
/usr/bin/tmux kill-session -t led-relay
/usr/bin/tmux new-session -d -s websocket 'cd /home/pi/outdoor-lights/controller; python3.6 ./websocket.py'
/usr/bin/tmux new-session -d -s led-relay 'cd /home/pi/outdoor-lights/controller/led_control/; python3.6 led_relay.py'
