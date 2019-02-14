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
	if (bool(settings['solid-strip'])):
		tpt /= 4 # Trigger more often to make rainbow smoother
		if (time % tpt == 0):
			curr_color = tuple(c / 255 for c in pixels[0])
			curr_color = colorsys.rgb_to_hls(*curr_color)
			new_color = ((curr_color[0] + 1 / 360) % 1, curr_color[1], curr_color[2])
			new_color = tuple(c * 255 for c in colorsys.hls_to_rgb(*new_color))
			fill(new_color)
	else:
		pos = time % len(pixels)
		step = int(settings['frequency']) / len(pixels)
		for i in range(len(pixels)):
			ind = (i + pos) % len(pixels)
			hue = (i * step) % 1
			rgb = tuple(c * 255 for c in colorsys.hls_to_rgb(hue, 1, 1))
			pixels[ind] = rgb
