import colorsys
import random

def lookup(name):
	print(name)
	if (name == 'solid-color'):
		return solid
	elif (name == 'rainbow'):
		return rainbow
	elif (name == 'snow'):
		return snow
	elif (name == 'runner'):
		return runner
	else:
		return red

def red(settings, time, pixels):
	fill(pixels, (255, 0, 0))

def fill(pixels, color):
	for i in range(len(pixels)):
		pixels[i] = color

def solid(settings, time, pixels, pixel_settings):
	color = (int(settings['red']), int(settings['green']), int(settings['blue']))
	fill(pixels, color)

def rainbow(settings, time, pixels, pixel_settings):
	speed = int(settings['speed'])
	hue_diff = int(settings['frequency']) / len(pixels) # The difference in hue from pixel n and n - 1
	
	if (speed != 0):
		spx = 1 / int(settings['speed']) # seconds / pixel
		hpt = hue_diff / spx / int(settings['tps']) # hue per tick
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

def snow(settings, time, pixels, pixel_settings):
	num_ticks = int(settings['tps']) * int(settings['duration'])
	brightness_diff = 510 / num_ticks
	threshold = float(settings['frequency']) / num_ticks
	
	for i in range(len(pixels)):
		if (pixel_settings[i] != 0):
			if (i == 0):
				print(pixels[i])
			pixel_settings[i] += 1
			if (pixel_settings[i] < num_ticks / 2):
				brightness = brightness_diff * pixel_settings[i]
				pixels[i] = (brightness, brightness, brightness)
			elif (pixel_settings[i] < num_ticks):
				brightness = brightness_diff * (num_ticks - pixel_settings[i])
				pixels[i] = (brightness, brightness, brightness)
			else:
				pixel_settings[i] = 0
		else:
			rand = random.random()
			if (rand < threshold):
				pixel_settings[i] = 1
				pixels[i] = tuple(c + brightness_diff for c in pixels[i])

def runner(settings, time, pixels, pixel_settings):
	color = (int(settings['red']), int(settings['green']), int(settings['blue']))
	tpt = 1 / int(settings['speed']) * int(settings['tps'])
	length = int(settings['length'])
	head = (time // tpt) % len(pixels)
	tail = (head - length + len(pixels)) % len(pixels)
	for i in range(len(pixels)):
		if (tail > head and (i > tail or i <= head)):
				pixels[i] = color
		elif (tail <= head and (i > tail and i <= head)):
				pixels[i] = color
		else:
			pixels[i] = (0, 0, 0)
