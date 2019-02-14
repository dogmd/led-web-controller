import effects
import json
import colorsys

class EffectController:
    def __init__(self, num_pixels):
        import_settings()
		self.effects = []
        for i in range(num_pixels):
            self.pixels.append((0, 0, 0))
        self.time = 0

    def import_settings():
        with open('settings.json', 'r') as settings:
            data = settings.read()
        self.settings = json.loads(data)
        
        for effect_name, effect_settings in self.settings['effects'].items():
            if (effect_settings['selected'] == 'true'):
                self.effects.append((effects.lookup(effect_name), effect_settings))

        self.pixels = []
        self.brightness = float(self.settings['powerSettings']['brightness']) / 100
        if (self.settings['powerSettings']['isOn'] == 'false'):
            self.brightness = 0

    def step(self):
		for effect in self.effects:
			effect[0](effects[1], self.time, self.pixels) # effect[0] is callback, effect[1] is effect settings
        apply_brightness()
        self.time += 1

    def apply_brightness(self):
		for i, color in enumerate(self.pixels):
			hls = colorsys.rgb_to_hls(*color)
			hls[1] *= self.brightness
			self.pixels[i] = colorsys.hls_to_rgb(*hls)
