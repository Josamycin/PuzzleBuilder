# Python Program to create a puzzle by dividing an image into an n by m grid of tiles and then randomising them.
# Currently works best with exact divisors of the number of pixels. 
# For example images that are 4032 pixels by 3024 pixels come out better when tiled to a four by four grid. 

import random
import tkinter as tk
from tkinter import filedialog
import numpy as np
from PIL import Image

# Filepath and prefix for the images created. The tiled photos can be deleted later.
# Having this be a dedicated directory makes file deletion easier. 
# This could be something like r'C:\Users\Josamycin\DeletableImages\Image_'
# The first image created would be: C:\Users\Josamycin\DeletableImages\Image_000.png
prefix = r'<prefix path>'

# output filename
# This should be the filepath and the name with the extension. 
# Somethinglike: r'C:\Users\Josamycin\KeepableImages\Image.png'
output = r'<output path>'

image1path = filedialog.askopenfilename()

# Load your image using PIL
image1 = Image.open(image1path)  # Replace with your actual image path

# Convert the PIL image to a NumPy array
im_array = np.array(image1)
im = np.array(image1)

def get_concat_h(im1, im2):
    dst = Image.new('RGB', (im1.width + im2.width, im1.height))
    dst.paste(im1, (0, 0))
    dst.paste(im2, (im1.width, 0))
    return dst

def get_concat_v(im1, im2):
    dst = Image.new('RGB', (im1.width, im1.height + im2.height))
    dst.paste(im1, (0, 0))
    dst.paste(im2, (0, im1.height))
    return dst

# Update the values of m and n accordingly. 
# Works best if m and n are exact divisors of the height and width and n*m < 1000.
# When m = n, aspect ratio of each tile is the same as the original image. 
m = 4 # if the resolution heights ends in zero consider changing to 5 or 10
n = 4 # if the resolution heights ends in zero consider changing to 5 or 10
M = round(image1.height/m)
N = round(image1.width/n)

# Set your desired tile dimensions
# tiles = [im_array[x:x+M, y:y+N] for x in range(0, im_array.shape[0], M) for y in range(0, im_array.shape[1], N)]
tiles = [im[x:x+M,y:y+N] for x in range(0,im.shape[0],M) for y in range(0,im.shape[1],N)]
i = 1000

for tile in tiles:
    suffix = str(i)[1:]
    tile_array = tile
    pil_image = Image.fromarray(tile_array)
    pil_image.save(prefix+suffix+".png")
    i = 1 + i
    # print('image_'+suffix+' height: ' + str(pil_image.height))
    # print('image_'+suffix+' width: ' + str(pil_image.width))

s = list(range(len(tiles)))
random.shuffle(s)

# suffix is the number appended to the end of each tile image
suffix = str(1000+s[0])[1:]

image1image = Image.open(prefix+suffix+".png")
# print('image1image: ' + prefix + suffix + '.png')

for j in range(1,n): # len(s)):
    suffix = str(1000+s[j])[1:]
    image2image = Image.open(prefix+suffix+".png")
    image1image = get_concat_h(image1image,image2image)
    # print('image2image'+str(j) + ': ' + prefix + suffix + '.png')

for k in range(1,m):
    suffix = str(1000+s[n*k])[1:]
    image3image = Image.open(prefix+suffix+".png")
    for j in range((k*n)+1,(k*n)+n): # len(s)):
        suffix = str(1000+s[j])[1:]
        image2image = Image.open(prefix+suffix+".png")
        image3image = get_concat_h(image3image,image2image)
        # print('image2image'+str(j) + ': ' + prefix + suffix + '.png')
    image1image = get_concat_v(image1image,image3image)
    
image1image.show()
image1image.save(output)
