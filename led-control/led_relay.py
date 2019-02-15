import time
import board
import adafruit_dotstar as dotstar
import effect_controller as ec

def main():
	# Using a DotStar Digital LED Strip with 30 LEDs connected to digital pins
	dots = dotstar.DotStar(board.D6, board.D5, 200, brightness=1, auto_write=False)
	n_dots = len(dots)
	effect = ec.EffectController(n_dots)
	delay = 0.05

	while True:
		effect.step()
		dots = effect.pixels
		dots.show()
		time.sleep(delay)

def update():
	ec.import_settings()
