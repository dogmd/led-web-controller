import effects
import json
import colorsys
import time
import inspect

DELAY = 0.025 # 40 tps

class EffectController:
    def __init__(self, num_pixels, settings_file='settings.json'):
        self.settings_file = settings_file

        self.effect_list = inspect.getmembers(effects, inspect.isfunction)
        self.effect_list = { f[0]: f[1] for f in self.effect_list }

        self.pixels = []
        for i in range(num_pixels):
            self.pixels.append((0, 0, 0))

        self.last_time = int(round(time.time() * 1000))
        self.time = 0
        self.import_settings()


    def import_settings(self):
        self.enabled_effects = []
        self.pixel_settings = []
        for i in range(len(self.pixels)):
            self.pixel_settings.append({})
        with open(self.settings_file, 'r') as settings:
            data = settings.read()
        self.settings = json.loads(data)

        # Effect settings
        for effect_name, effect_settings in self.settings['effects'].items():
            effect_settings['tps'] = 1 / DELAY
            effect_settings['strand-length'] = 20
            if (effect_settings['selected'] == 'true'):
                if (effect_name in self.effect_list):
                    self.enabled_effects.append((self.effect_list[effect_name], effect_settings))
                else:
                    # Solid magenta strip is "error" state
                    print('Error, {} effect was not found'.format(effect_name))
                    self.enabled_effects.append((effects.magenta, effect_settings))

        # Power settings
        self.brightness = float(self.settings['powerSettings']['brightness']) / 100
        if (self.settings['powerSettings']['isOn'] == 'false'):
            self.brightness = 0

    def step(self):
        # Apply the effects
        for effect in self.enabled_effects:
            effect[0](effect[1], self.time, self.pixels, self.pixel_settings) # effect[0] is callback, effect[1] is effect settings
        self.apply_brightness()
        for ind in range(len(self.pixels)):
            color = self.pixels[ind]
            color = tuple(int(c) % 256 for c in color)
            self.pixels[ind] = color
        
        
        time.sleep(max(0, DELAY - (int(round(time.time() * 1000)) - self.last_time) / 1000))
        self.last_time = int(round(time.time() * 1000))
        
        self.time += 1


    # Reduce the brightness of rgb
    def apply_brightness(self):
        for i, color in enumerate(self.pixels):
            color = tuple(c / 255 for c in color)
            hls = colorsys.rgb_to_hls(*color)
            hls = (hls[0], hls[1] * self.brightness, hls[2])
            self.pixels[i] = tuple(c * 255 for c in colorsys.hls_to_rgb(*hls))
