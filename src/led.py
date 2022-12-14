from __future__ import print_function
from __future__ import division

import numpy as np
import config
import platform

from lifxlan import LifxLAN


"""Try to fetch all lights based on order from config"""
try:
    lifx = LifxLAN(config.NUM_LIGHTS)
    all_devices = lifx.get_lights()
    devices = []

    print('\nLIFX Devices:')
    for name in config.ORDER_LIGHTS:
        for device in all_devices:
            label = device.get_label()
            if label == name:
                devices.append(device)
                device.set_power('on')
                print("    {} connected!".format(label))

    # for name in config.ORDER_LIGHTS:
        # device = lifx.get_device_by_name(name)
        # devices.append(device)

        # device.set_power('on')
        # rint("    {} connected!".format(device.get_label()))
except:
    print('LIFX Devices not found!')
    exit()
    

_gamma = np.load(config.GAMMA_TABLE_PATH)
"""Gamma lookup table used for nonlinear brightness correction"""

_prev_pixels = np.tile(253, (3, config.N_PIXELS))
"""Pixel values that were most recently displayed on the LED strip"""

pixels = np.tile(1, (3, config.N_PIXELS))
"""Pixel values for the LED strip"""

_is_python_2 = int(platform.python_version_tuple()[0]) == 2

def on():
    try:
        lifx.set_power_all_lights('on')
    except:
        print('LIFX Devices not found!')

def off():
    try:
        lifx.set_power_all_lights('off')
    except:
        print('LIFX Devices not found!')

def update():
    global pixels, _prev_pixels
    # Truncate values and cast to integer
    pixels = np.clip(pixels, 0, 255).astype(int)
    # Optional gamma correction
    p = _gamma[pixels] if config.SOFTWARE_GAMMA_CORRECTION else np.copy(pixels)
    # Read the rgb values
    r = p[0][:].astype(int)
    g = p[1][:].astype(int)
    b = p[2][:].astype(int)

    # Change colors based on each light postition
    if config.FLAT_MODE:
        color = RGBtoHSBK((r[50],g[50],b[50]))
        lifx.set_color_all_lights(color, rapid=True)
    else:        
        for i in range(config.NUM_LIGHTS):
            position = int((config.N_PIXELS / config.NUM_LIGHTS+1)) * (i+1)
            color = RGBtoHSBK((r[position],g[position],b[position]))
            devices[i].set_color(color, rapid=True)


    """ OLD METHOD """
    # part = (config.N_PIXELS // 2)
    # piece = part // (len(lights) // 2 + 1)

    # if len(lights) == 1:
    #     color = RGBtoHSBK((r[part],g[part],b[part]))
    # elif len(lights) % 2 == 0:
    #     for i in range(len(lights)):
    #         position = part + (piece*(i//2))
    #         color = RGBtoHSBK((r[position],g[position],b[position]))
    #         fcolor[i] = color
    # else:  
    #     for i in range(len(lights)):
    #         position = part + (piece*((i//2)+1))
    #         color = RGBtoHSBK((r[position],g[position],b[position]))
    #         fcolor[i] = color


def RGBtoHSBK (RGB, temperature = 3500):
    cmax = max(RGB)
    cmin = min(RGB)
    cdel = cmax - cmin

    # Bound brightness by +/- 100
    brightness = int((cmax/255) * config.MAX_BRIGHTNESS) + 100
    if brightness > 65535:
        brightness = 65535
    elif brightness < 100:
        brightness = 100

    if cdel != 0:
        saturation = int(((cdel) / cmax) * (config.MAX_SATURATION / 2))

        redc = (cmax - RGB[0]) / (cdel)
        greenc = (cmax - RGB[1]) / (cdel)
        bluec = (cmax - RGB[2]) / (cdel)

        if RGB[0] == cmax:
            hue = bluec - greenc
        else:
            if RGB[1] == cmax:
                hue = 2 + redc - bluec
            else:
                hue = 4 + greenc - redc

        hue = hue / 6
        if hue < 0:
            hue = hue + 1

        hue = int(hue*65535)
    else:
        saturation = 0
        hue = 0

    color = [hue, saturation, brightness, temperature]
    return color


""" TEST LED.PY """
# Execute this file to run a LED strand test
# If everything is working, you should see a red, green, and blue pixel scroll
# across the LED strip continuously
if __name__ == '__main__':    
    # Turn all pixels off
    pixels *= 0
    pixels[0, 0] = 255  # Set 1st pixel red
    pixels[1, 1] = 255  # Set 2nd pixel green
    
    print('Starting LED strand test')
    update()
   