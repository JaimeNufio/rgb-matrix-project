import time
import random
import sys
from rgbmatrix import RGBMatrix, RGBMatrixOptions
from PIL import Image
from util import Tetronimo

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
options.brightness = 50

matrix = RGBMatrix(options=options)
canvas = matrix.CreateFrameCanvas()

# state = [ [False for i in range(32)] for i in range(32) ]
# print(state)

# def updateState (pixels):
#     for pixel in pixels:
#         if not state[pixel[0],pixel[1]]:
#             state[pixel[0],pixel[1]] = True

# Pixels that will no longer move.
setPixels = []

def updateSetPixels(newPixels):
    for pixel in newPixels:
        if pixel not in setPixels:
            setPixels.append(pixel)

def reset():
    global setPixels

    time.sleep(.25)    
    setPixels = []
    canvas.Clear()
    matrix.SwapOnVSync(canvas)   


def createPiece():
    global pieces
    pieces.append(Tetronimo.Tetronimo(canvas,matrix,
    'RANDOM',                       # what piece
    len(pieces),                    # id
    random.randint(0,3),            # rotation
    [random.randint(0,32-4),-10]    # pos
    ))


pieces = []


frame = 0
try:
    print("Press C-C to stop.")
    while True:

        if len(pieces) < 1:
            createPiece()
        frame+=1
        toRemove = []
        for piece in pieces:
            if piece.locked:
                print('this piece was locked')
                toRemove.append(piece.getId())
                updateSetPixels(piece.getLockedState())
                continue

            piece.moveDown(canvas,matrix,setPixels)

        # if frame % 5:
        #     LPiece.changeRotation(canvas,matrix,frame%4)
        time.sleep(.001)

        for pixel in setPixels:
            if pixel[1] <= 0:
                reset()
                continue

        pieces = [p for p in pieces if p.getId() not in toRemove]
        print('# active pieces:',len(pieces))


except KeyboardInterrupt:
    sys.exit(0)
