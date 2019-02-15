import time
#import random
#import board
#import adafruit_dotstar as dotstar
import effect_controller as ec
#
## Using a DotStar Digital LED Strip with 30 LEDs connected to digital pins
#dots = dotstar.DotStar(board.D6, board.D5, 200, brightness=1, auto_write=False)
n_dots = 200
effect = ec.EffectController(n_dots)
delay = 0.05

while True:
	effect.step()
	#for dot in range(n_dots):
	#	dots[dot] = effect.pixels[dot]
	#dots.show()
	time.sleep(delay)

def tps():
	return 1 / delay
