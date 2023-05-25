#!/bin/env python

# REQUIREMENTS:
# imagemagick

# USAGE: 
# `convert $IMAGE -colorspace gray +matte -depth 2 -colors 4 pgm:- | ./img_to_bytearray.py`
# upload 'out' file to Pico
# load `bytearray(open('out', 'rb').read())` into buffer_4Gray and call the display method 

import sys
from pathlib import Path
import time
import subprocess

fileDir = Path(__file__).parent.resolve()

def convert(image):
    p = subprocess.Popen(['convert', image, '-colorspace', 'gray', '+matte', '-depth', '2', '-colors', '4', '-resize', '280x200!', 'pgm:-'], 
                         stderr=subprocess.STDOUT, stdout=subprocess.PIPE)
    pixels = p.stdout.readlines()[3].decode('utf-8')
    colours = [] # enumerate 4 gray levels
    for p in pixels:
        if not p in colours:
            colours.append(p)
            if len(colours) == 4:
                break

    colours = sorted(colours) # sort from low to high

    BLACK = '00'
    DARK_GRAY = '10'
    LIGHT_GRAY = '01'
    WHITE = '11'

    pixels = pixels.replace(colours[0],BLACK)\
                            .replace(colours[1],DARK_GRAY)\
                            .replace(colours[2],LIGHT_GRAY)\
                            .replace(colours[3],WHITE)

    plist = []
    fourc = [pixels[i:i+8] for i in range(0, len(pixels), 8)] # split pixel values into 8 bit packets
    for byte in fourc:
        plist.append(int(byte[::-1], 2)) # append reversed bytes to list
    b = bytearray(plist) # bytearray from list

    with open(f'{fileDir}/out', 'wb') as f:
        f.write(b) # write bytearray to file 'out'
        f.close()
    return

if __name__ == '__main__':
    # convert('in.jpg')
    convert(f'{fileDir}/../gas_station_display/e5.png')


# RESOURCES
# https://stackoverflow.com/questions/35797988/converting-images-to-indexed-2-bit-grayscale-bmp
# https://www.waveshare.com/wiki/Pico-ePaper-3.7