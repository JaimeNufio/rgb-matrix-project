import time
import sys
from rgbmatrix import RGBMatrix, RGBMatrixOptions
from PIL import Image
from util import ImageManipulate

xDim = 64
yDim = 64 
scale = 5

imageFile = "assets/img.jpg"
image = ImageManipulate.cropCenter(Image.open(imageFile),xDim*scale,yDim*scale)

options = RGBMatrixOptions()
options.rows = xDim
options.cols = yDim
options.gpio_slowdown = 4
options.chain_length = 1
options.parallel = 1
options.hardware_mapping = 'adafruit-hat'
options.brightness = 50

matrix = RGBMatrix(options=options)

image.thumbnail((matrix.width,matrix.height),Image.ANTIALIAS)
matrix.SetImage(image.convert('RGB'))

try:
    print("Press C-C to stop.")
    while True:
        time.sleep(100)
except KeyboardInterrupt:
    sys.exit(0)