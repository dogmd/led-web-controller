import colorsys
import random

tps = 20

def lookup(name):
	if (name == 'solid-color'):
		return solid
	elif (name == 'rainbow'):
		return rainbow

def fill(pixels, color):
	for ind in range(len(pixels)):
		pixels[ind] = color

def solid(settings, time, pixels):
	color = (int(settings['red']), int(settings['green']), int(settings['blue']))
	fill(pixels, color)

def rainbow(settings, time, pixels):
	tpt = tps / int(settings['speed']) # ticks per trigger
	print(pixels[0])
	if (bool(settings['solid-strip'])):
		tpt /= 4 # Trigger more often to make rainbow smoother
		if (time % tpt == 0):
			curr_color = tuple(c / 255 for c in pixels[0])
			curr_color = colorsys.rgb_to_hls(*curr_color)
			new_color = ((curr_color[0] + 1 / 360) % 1, 0.5, 1)
			new_color = tuple(c * 255 for c in colorsys.hls_to_rgb(*new_color))
			fill(pixels, new_color)
	else:
		pos = (time // tpt) % len(pixels)
		step = int(settings['frequency']) / len(pixels)
		for i in range(len(pixels)):
			ind = int(i + pos) % len(pixels)
			hue = (i * step) % 1
			rgb = tuple(c * 255 for c in colorsys.hls_to_rgb(hue, 0.5, 1))
			pixels[ind] = rgb

def snow(settings, time, pixels):
	num_ticks = tps * settings['duration']
	tpt = 254 // num_ticks
	threshold = (int(settings['frequency']) / 100) / 4 # Max probability is 25%
	for ind in range(len(pixels)):
		color = pixels[ind]
		r = int(color[0])
		g = int(color[1])
		b = int(color[2])
		if (r == b and b == g and r != 0):
			if (time % tpt == 0):
				print(r)
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
