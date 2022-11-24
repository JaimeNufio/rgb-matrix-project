from rgbmatrix import RGBMatrix, RGBMatrixOptions

class Tetronimo:
    pos = (0,0)
    shapeArray = [
        [0,0,0,0,],
        [0,0,0,0,],
        [0,0,0,0,],
        [0,0,0,0,],
    ] #2d array?
    rotation = 0 # 1: 90 deg, 2: 180 deg, 3: 270 
    color = 0
    matrix = None

    def drawAt(pos):
        for x in range(4):
            for y in range(4):
                matrix.drawPixel(pos[0]+x, pos[1]+y, this.color);


    def __init__(self,matrix,shape,pos=(0,0)):
        if shape == 'LINE':
            self.color = (0,240,240)
            self.shapeArray = [
                [1,1,1,1,],
                [0,0,0,0,],
                [0,0,0,0,],
                [0,0,0,0,],
            ]
        else:
            self.color = (0,240,240)
            self.shapeArray = [
                [1,1,1,1,],
                [0,0,0,0,],
                [0,0,0,0,],
                [0,0,0,0,],
            ]
        self.pos = pos
        self.matrix = matrix
        self.drawAt(([0,0]))
        



    # CAN DRAW FLOW:
    # 1 - Calculate next position
    # 2 - Check 'collision map' (parent class? adjacent)
    # 3 - draw
    # 4 - update collision map