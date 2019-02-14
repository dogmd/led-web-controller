import time
import random
import board
import adafruit_dotstar as dotstar

# Using a DotStar Digital LED Strip with 30 LEDs connected to digital pins
dots = dotstar.DotStar(board.D6, board.D5, 200, brightness=1, auto_write=False)
n_dots = len(dots)
effect = EffectController(n_dots)

while True:
	effect.step()
	for dot in range(n_dots):
		dots[dot] = effect.pixels[dot]
	dots.show()
	time.sleep(.25)
