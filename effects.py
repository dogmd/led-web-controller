import colorsys
import random
import inspect

def magenta(settings, time, pixels, pixel_settings):
    fill(pixels, (255, 0, 255))

def fill(pixels, color):
    for i in range(len(pixels)):
        pixels[i] = color

def time2ticks(secs, tps):
    return max(secs * tps, 1)

def solid(settings, time, pixels, pixel_settings):
    color = (int(settings['red']), int(settings['green']), int(settings['blue']))
    fill(pixels, color)

def rainbow(settings, time, pixels, pixel_settings):
    speed = int(settings['speed'])
    hue_diff = int(settings['frequency']) / len(pixels) # The difference in hue from pixel n and n - 1
    hpt = hue_diff * speed / int(settings['tps']) # hue per tick

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

def snow(settings, time, pixels, pixel_settings, twinkle=False, full_strip=False):
    num_ticks = time2ticks(float(settings['duration']), int(settings['tps']))
    threshold = 0
    if (not full_strip):
        threshold = float(settings['frequency']) / num_ticks
    color = (0, 0, 0)
    hls = (0, 0, 0)
    if (not twinkle):
        brightness_diff = 2 / num_ticks
        color = (int(settings['red']), int(settings['green']), int(settings['blue']))
        color = tuple(c / 255 for c in color)
        hls = colorsys.rgb_to_hls(*color)
    if (full_strip):
        brightness_diff = (1 - hls[1]) / num_ticks

    for i in range(len(pixels)):
        if (twinkle):
            color = pixels[i]
            brightness_diff = 2 / num_ticks
            color = tuple(c / 255 for c in color)
            hls = colorsys.rgb_to_hls(*color)
        if ('snow' in pixel_settings[i]):
            pixel_settings[i]['snow'] += 1
            brightness = 0
            if (pixel_settings[i]['snow'] < num_ticks / 2):
                brightness = brightness_diff * pixel_settings[i]['snow']
            elif (pixel_settings[i]['snow'] < num_ticks):
                brightness = brightness_diff * (num_ticks - pixel_settings[i]['snow'])
            else:
                pixel_settings[i].pop('snow')
            if (brightness >= 1):
                brightness = 1 - brightness_diff
            if (brightness <= 0):
                brightness = brightness_diff
            new_hls = (hls[0], brightness, hls[2])
            new_color = colorsys.hls_to_rgb(*new_hls)
            new_color = tuple(c * 255 for c in new_color)
            pixels[i] = new_color
        else:
            rand = random.random()
            if (rand < threshold or full_strip):
                pixel_settings[i]['snow'] = 1
                if (twinkle):
                    pixels[i] = (0, 0, 0)
                else:
                    pixels[i] = tuple(c + brightness_diff for c in pixels[i])
            else:
                pixels[i] = (0, 0, 0)

def runner(settings, time, pixels, pixel_settings, overwrite=True):
    color = (int(settings['red']), int(settings['green']), int(settings['blue']))
    tpt = time2ticks(1 / int(settings['speed']), int(settings['tps']))
    length = int(settings['length'])
    head = (time // tpt) % len(pixels)
    tail = (head - length + len(pixels)) % len(pixels)
    for i in range(len(pixels)):
        pixel_settings[i]['runner'] = pixels[i]
        if (tail > head and (i > tail or i <= head)):
                pixels[i] = color
        elif (tail <= head and (i > tail and i <= head)):
                pixels[i] = color
        else:
            if (overwrite):
                pixels[i] = (0, 0, 0)
            else:
                pixels[i] = pixel_settings[i]['runner']

def patriot(settings, time, pixels, pixel_settings):
    speed = int(settings['speed'])
    if (speed != 0):
        tpt = time2ticks(1 / int(settings['speed']), int(settings['tps']))
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
        for i in range(len(colors)):
            color = int(colors[i], 16)
            rgb = (color >> 16, color >> 8 & 0xFF, color & 0xFF) 
            segments.append(rgb)

        for i in range(len(pixels)):
            pixels[i] = segments[int(i / len(pixels) * len(segments))]
    else:
        fill(pixels, (0, 0, 0))

def wipe(settings, time, pixels, pixel_settings):
    if (settings['full-strip'] == 'true'):
        tpt = time2ticks(1 / int(settings['speed']), int(settings['tps']))
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
    else:
        runner(settings, time, pixels, pixel_settings, False)

def twinkle(settings, time, pixels, pixel_settings, duration=1, full_strip=False):
    if (full_strip):
        settings['duration'] = duration
    snow(settings, time, pixels, pixel_settings, True, full_strip)

def breathe(settings, time, pixels, pixel_settings):
    twinkle(settings, time, pixels, pixel_settings, 1 / float(settings['speed']), True)

def blink(settings, time, pixels, pixel_settings):
    off_ticks = time2ticks(float(settings['off-time']),int(settings['tps']))
    on_ticks = time2ticks(float(settings['on-time']), int(settings['tps']))
    if ('blink' in pixel_settings[0]): # Strip is off
        if (time > pixel_settings[0]['blink'] + off_ticks):
            pixel_settings[0].pop('blink')
        else:
            for i in range(len(pixels)):
                pixels[i] = (0, 0, 0)

    else:
        if (time % (on_ticks + 1) == 0):
            pixel_settings[0]['blink'] = time
