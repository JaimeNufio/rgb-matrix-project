import time
import sys
from rgbmatrix import RGBMatrix, RGBMatrixOptions
from PIL import Image
from util import ImageManipulate
import os
import glob

arr = os.listdir()
xDim = 64
yDim = 64 
scale = 5

options = RGBMatrixOptions()
options.rows = xDim
options.cols = yDim
options.gpio_slowdown = 4
options.chain_length = 1
options.parallel = 1
options.hardware_mapping = 'adafruit-hat'
options.brightness = 25

matrix = RGBMatrix(options=options)

for filenum in range(1,6562):
# imageFile = "assets/img.jpg"

    if (filenum % 2 == 0 or filenum % 3 == 0):
        continue

    adapt_filenum = str(filenum)

    if (filenum < 100 ):
        adapt_filenum = "0"+(adapt_filenum)
    if (filenum < 10):
                adapt_filenum = "0"+(adapt_filenum)

    imageFile = "assets/BadApple/bad_apple_"+adapt_filenum+".png"#filename
    image = ImageManipulate.cropCenter(Image.open(imageFile),xDim*scale,yDim*scale)
    image = Image.open(imageFile)
    print(imageFile)

    image.thumbnail((matrix.width,matrix.height),Image.ANTIALIAS)
    matrix.SetImage(image.convert('RGB'))
    time.sleep(1/32)