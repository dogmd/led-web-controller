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
	elif (name == 'patriot'):
		return patriot
	elif (name == 'custom'):
		return custom
	elif (name == 'wipe'):
		return wipe
	elif (name == 'twinkle'):
		return twinkle
	else:
		return magenta

def magenta(settings, time, pixels, pixel_settings):
	fill(pixels, (255, 0, 255))

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
		if ('snow' in pixel_settings[i]):
			pixel_settings[i]['snow'] += 1
			if (pixel_settings[i]['snow'] < num_ticks / 2):
				brightness = brightness_diff * pixel_settings[i]['snow']
				pixels[i] = (brightness, brightness, brightness)
			elif (pixel_settings[i]['snow'] < num_ticks):
				brightness = brightness_diff * (num_ticks - pixel_settings[i]['snow'])
				pixels[i] = (brightness, brightness, brightness)
			else:
				pixel_settings[i].pop('snow')
		else:
			rand = random.random()
			if (rand < threshold):
				pixel_settings[i]['snow'] = 1
				pixels[i] = tuple(c + brightness_diff for c in pixels[i])
			else:
				pixels[i] = (0, 0, 0)

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

def patriot(settings, time, pixels, pixel_settings):
	speed = int(settings['speed'])
	if (speed != 0):
		tpt = 1 / int(settings['speed']) * int(settings['tps'])
		pos = (time // tpt) % len(pixels)
	else:
		pos = 0
	strand_length = int(settings['strand-length'])

	for i in range(len(pixels)):
		relative_pos = (i + pos) % len(pixels)
		if (settings['solid-strand'] == 'true'):
			if (relative_pos // strand_length % 3 == 0):
				pixels[i] = (255, 0, 0)
			if (relative_pos // strand_length % 3 == 1):
				pixels[i] = (255, 255, 255)
			if (relative_pos // strand_length % 3 == 2):
				pixels[i] = (0, 0, 255)
		else:
			if (relative_pos % 3 == 0):
				pixels[i] = (255, 0, 0)
			if (relative_pos % 3 == 1):
				pixels[i] = (255, 255, 255)
			if (relative_pos % 3 == 2):
				pixels[i] = (0, 0, 255)

def custom(settings, time, pixels, pixel_settings):
	if ('colors' in settings):
		colors = settings['colors']
		segments = []
		strand_length = int(settings['strand-length'])
		for i in range(len(colors)):
			color = int(colors[i], 16)
			rgb = (color >> 16, color >> 8 & 0xFF, color & 0xFF) 
			segments.append(rgb)

		for i in range(len(pixels)):
			pixels[i] = segments[i // strand_length]
	else:
		fill(pixels, (0, 0, 0))

def wipe(settings, time, pixels, pixel_settings):
	tpt = 1 / int(settings['speed']) * int(settings['tps'])
	pos = int((time // tpt) % len(pixels))
	color = (int(settings['red']), int(settings['green']), int(settings['blue']))
	if ('wipe' not in pixel_settings[-1]): # Grow the color wipe
		for i in range(pos + 1):
			pixel_settings[i]['wipe'] = pixels[i]
			pixels[i] = color
	else: # Shrink the color wipe
		for i in range(len(pixels)):
			if (i <= pos):
				if ('wipe' in pixel_settings[i]):
					old_color = pixel_settings[i].pop('wipe')
					pixels[i] = old_color
			else:
				pixels[i] = color

def twinkle(settings, time, pixels, pixel_settings):
	num_ticks = int(settings['tps'])
	threshold = float(settings['frequency']) / num_ticks
	for i in range(len(pixels)):
		if ('twinkle' in pixel_settings[i]):
			if ('twinkle_diff' not in pixel_settings[i]):
				rgb = tuple(c / 255 for c in pixels[i])
				brightness = colorsys.rgb_to_hls(*rgb)[1]
				pixel_settings[i]['twinkle_diff'] = (1 - brightness) / num_ticks * 2
			else:
				pixel_settings[i]['twinkle'] += 1
				brightness_diff = pixel_settings[i]['twinkle_diff']
				tick_pos = pixel_settings[i]['twinkle']
				rgb = tuple(c / 255 for c in pixels[i])
				hls = colorsys.rgb_to_hls(*rgb)
				brightness_offset = 0

				if (tick_pos < num_ticks / 2):
					brightness_offset = brightness_diff * tick_pos
				elif (tick_pos < num_ticks):
					brightness_offset = brightness_diff * (num_ticks - tick_pos)
				else:
					pixel_settings[i].pop('twinkle')
					pixel_settings[i].pop('twinkle_diff')

				new_brightness = hls[1] + brightness_offset
				if (new_brightness >= 1): # For some reason, the color distinctly changes with brightness 1, so avoid that
					new_brightness = new_brightness - brightness_diff
				hls = (hls[0], new_brightness, hls[2])
				pixels[i] = tuple(c * 255 for c in colorsys.hls_to_rgb(*hls))
		else:
			rand = random.random()
			if (rand < threshold):
				pixel_settings[i]['twinkle'] = 0

