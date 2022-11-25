import time
import random
import sys
from rgbmatrix import RGBMatrix, RGBMatrixOptions
from PIL import Image
from util import ImageManipulate

xDim = 64
yDim = 64 
scale = 5

# imageFile = "assets/img.jpg"
# image = ImageManipulate.cropCenter(Image.open(imageFile),xDim*scale,yDim*scale)

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

state = []
gen = 0

for i in range(32):
    state.append([False for element in range(32)])

#co-ords
def drawPixelOnGrid(xPos,yPos,turnOn):
    global state
    offsetX = 2*xPos
    offsetY = 2*yPos
    state[xPos][yPos] = turnOn
    for x in range(2):
        for y in range(2):
            canvas.SetPixel(offsetX+x,offsetY+y,255*turnOn,255*turnOn,255*turnOn)

def kernel(xPos,yPos):
    count = 0
    for x in [-1,0,1]:
        for y in [-1,0,1]:
            if (x == 0 and y == 0 ):
                continue # don't count yourself as a neigbor
            try:
                if state[xPos+x][yPos+y]:
                    count += 1
                    # print('neighbor @',xPos+x,yPos+y)
            except:
                count += 0
    return count

def runKernel():
    toDie = []
    toBorn = []
    for x in range(32):
        for y in range(32):
            neighbors = kernel(x,y) 
            if neighbors < 2 or neighbors > 3:
                toDie.append([x,y])
            elif neighbors == 3:
                toBorn.append([x,y])
                # drawPixelOnGrid(x,y,True)

    # print(toDie)

    for i in (toDie):
        drawPixelOnGrid(i[0],i[1],False)
    for i in (toBorn):
        drawPixelOnGrid(i[0],i[1],True)

    matrix.SwapOnVSync(canvas)

def countAlive():
    global state

    count = 0
    for x in range(32):
        for y in range(32):
            count += state[x][y]
    return count

#percent represents what percent random fill we want
def randomFill(percent):
    global state,gen

    gen = 0 

    #flash briefly.
    for x in range(32):
        for y in range(32):
            drawPixelOnGrid(x,y,False)
    time.sleep(.15)
    matrix.SwapOnVSync(canvas)
    for x in range(32):
        for y in range(32):
            drawPixelOnGrid(x,y,True)
    time.sleep(.15)
    matrix.SwapOnVSync(canvas)
    for x in range(32):
        for y in range(32):
            drawPixelOnGrid(x,y,False)
    time.sleep(.15)
    matrix.SwapOnVSync(canvas)
    for x in range(32):
        for y in range(32):
            drawPixelOnGrid(x,y,True)
    time.sleep(.15)
    for x in range(32):
        for y in range(32):
            drawPixelOnGrid(x,y,False)
    matrix.SwapOnVSync(canvas)

    cnt=0
    for x in range(32):
        for y in range(32):
            ah = random.random()
            if ah > 1-percent:
                cnt+=1
                drawPixelOnGrid(x,y,True)
    print("fill:",cnt)
    matrix.SwapOnVSync(canvas)

        

def drawGliderAt(xPos,yPos):
    # drawPixelOnGrid(xPos,yPos,True)
    drawPixelOnGrid(xPos+1,yPos,True)
    drawPixelOnGrid(xPos+2,yPos+1,True)
    drawPixelOnGrid(xPos+0,yPos+2,True)
    drawPixelOnGrid(xPos+1,yPos+2,True)
    drawPixelOnGrid(xPos+2,yPos+2,True)


drawGliderAt(10,5)
drawGliderAt(15,10)
drawGliderAt(5,15)

# for x in range(8):
#     for y in range(8):
#         if random.random() > .3:
#             drawGliderAt(x,y)



# drawPixelOnGrid(0,31,True)
# drawPixelOnGrid(31,0,True)
# drawPixelOnGrid(12,12,True)
# drawPixelOnGrid(31,31,True)
matrix.SwapOnVSync(canvas)

try:
    print("Press C to stop.")
    gen = 0
    while True:
        gen+=1
        runKernel()
        if countAlive() < 10 or gen > 350:
            randomFill(.5)
            # exit(0)
        time.sleep(.1)
        print(gen)
except KeyboardInterrupt:
    sys.exit(0)