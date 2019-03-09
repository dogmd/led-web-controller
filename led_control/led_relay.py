import time
import board
import adafruit_dotstar as dotstar
import led_control.effect_controller as ec

# Using a DotStar Digital LED Strip with 30 LEDs connected to digital pins
dots = dotstar.DotStar(board.SCK, board.MOSI, 200, brightness=1, auto_write=False)
#dots = dotstar.DotStar(board.D26, board.D19, 200, brightness=1, auto_write=False)
n_dots = len(dots)
effect_controller = ec.EffectController(n_dots)

def main():
	effect_controller.step()
	for ind in range(n_dots):
		dots[ind] = effect_controller.pixels[ind]
	#print(dots[0])
	dots.show()

def update_settings():
	effect_controller.import_settings()
