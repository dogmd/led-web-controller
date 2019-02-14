def lookup(name):
	if (name == 'solid-color'):
		return solid

def solid(settings, time, pixels):
	color = (settings['red'], settings['green'], settings['blue'])
	for ind in range(len(pixels)):
		pixels[ind] = color
