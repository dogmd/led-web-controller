import colorsys
import random

tps = 20

def lookup(name):
	print(name)
	if (name == 'solid-color'):
		return solid
	elif (name == 'rainbow'):
		return rainbow
	elif (name == 'snow'):
		return snow
	else:
		return red

def red(settings, time, pixels):
	fill(pixels, (255, 0, 0))

def fill(pixels, color):
	for ind in range(len(pixels)):
		pixels[ind] = color

def solid(settings, time, pixels):
	color = (int(settings['red']), int(settings['green']), int(settings['blue']))
	fill(pixels, color)

def rainbow(settings, time, pixels):
	speed = int(settings['speed'])
	hue_diff = int(settings['frequency']) / len(pixels) # The difference in hue from pixel n and n - 1
	if (speed != 0):
		spx = 1 / int(settings['speed']) # seconds / pixel
		hpt = hue_diff / spx / tps # hue per tick
	else:
		hpt = 0 

	if (settings['solid-strip'] == 'true'):
		hue = (hpt * time) % 1
		rgb = tuple(c * 255 for c in colorsys.hls_to_rgb(hue, 0.5, 1))
		fill(pixels, rgb)
	else:
		first = hpt * time
		for i in range(len(pixels)):
			hue = (first + hue_diff * i) % 1
			rgb = tuple(c * 255 for c in colorsys.hls_to_rgb(hue, 0.5, 1))
			pixels[i] = rgb

def snow(settings, time, pixels):
	num_ticks = tps * int(settings['duration'])
	tpt = 254 // num_ticks
	threshold = float(settings['frequency']) / 4 # Max probability is 25%
	for ind in range(len(pixels)):
		color = pixels[ind]
		r = int(color[0])
		g = int(color[1])
		b = int(color[2])
		if (time % tpt == 0):
			if (r == b and b == g and r != 0):
					print(pixels[ind])
					# If current "brightness" value is even, that means its dimming, if its odd it is brightening
					if (r % 2 == 0):
						pixels[ind] = (r - 2, g - 2, b - 2)
					else:
						if (r == 253):
							pixels[ind] = (254, 254, 254)
						else:
							pixels[ind] = (r + 2, g + 2, b + 2)
			else:
				pixels[ind] = (0, 0, 0)
				rand = random.random()
				if (rand < threshold):
					pixels[ind] = (1, 1, 1) # Make it a snowflake
