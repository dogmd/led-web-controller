/usr/bin/tmux kill-session -t websocket
/usr/bin/tmux new-session -d -s websocket 'cd /home/pi/outdoor-lights/controller; python3.6 ./websocket.py'
