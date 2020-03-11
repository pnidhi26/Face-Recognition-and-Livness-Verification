import io, os
from PIL import Image, ImageDraw, ImageFont

# Compressing an big size image
def compress(filename):
    im = Image.open(filename)
    im.save(filename, optimize=True, quality=70) 





