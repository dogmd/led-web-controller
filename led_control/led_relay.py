import time
import board
import adafruit_dotstar as dotstar
import effect_controller as ec

# Using a DotStar Digital LED Strip with 30 LEDs connected to digital pins
dots = dotstar.DotStar(board.D6, board.D5, 200, brightness=1, auto_write=False)
n_dots = len(dots)
effect = ec.EffectController(n_dots)
delay = 0.05
ticks = 0

while True:
	effect.step()
	for ind in range(n_dots):
		dots[ind] = effect.pixels[ind]
	dots = effect.pixels
	dots.show()
	time.sleep(delay)
	ticks += 1
	if (ticks == 10):
		effect.import_settings()
		ticks = 0
