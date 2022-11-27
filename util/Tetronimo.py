import random
from rgbmatrix import RGBMatrix, RGBMatrixOptions


class Tetronimo:
    pos = [0,0]
    currentShapeArray = [[]] #2d array
    rotations = [[],[],[],[]]
    rotation = 0 # 1: 90 deg, 2: 180 deg, 3: 270 
    color = [0,0,0]
    locked = False
    lockedState = [[]]
    id = 0
    
    def __init__(self,canvas,matrix,shape,id,rotation,*pos):
        self.setShape(shape)
        self.pos = pos[0] 
        self.rotation = rotation
        self.setRotation(canvas,matrix,self.rotation)
        self.draw(canvas,matrix)  
        self.id = id

    def isLocked(self):
        return self.locked

    def getLockedState(self):
        return self.lockedState

    def getId(self):
        return self.id

    def deleteCurrent(self,canvas,matrix):
        for y in range(len(self.currentShapeArray)):
            for x in range(len(self.currentShapeArray[y])):
                if (self.currentShapeArray[y][x]):
                    # 'parent' of pixels are x*2,y*2
                    for pixelX in range(2):
                        for pixelY in range(2):
                            canvas.SetPixel(
                                x*2 + pixelX + 2*self.pos[0], 
                                y*2 + pixelY + 2*self.pos[1],
                                0,0,0)                   

    def draw(self,canvas,matrix):
        # print('drawAt',self.pos)
        for y in range(len(self.currentShapeArray)):
            for x in range(len(self.currentShapeArray[y])):
                if (self.currentShapeArray[y][x]):
                    # 'parent' of pixels are x*2,y*2
                    for pixelX in range(2):
                        for pixelY in range(2):
                            canvas.SetPixel(
                                x*2 + pixelX + 2*self.pos[0], 
                                y*2 + pixelY + 2*self.pos[1],
                                    *self.color)   
        matrix.SwapOnVSync(canvas)                

    def canFall(self,canvas,matrix,state):
        # print("coords of bottom Row:")
        # bottomRow = self.currentShapeArray[-1]
        # bottomRowIndex = len(self.currentShapeArray)-1
        # print('br',bottomRow)

        collisionChecks = []
        for y in range(len(self.currentShapeArray)):
            for x in range(len(self.currentShapeArray[y])):
            
                if (self.currentShapeArray[y][x]):
                    collide = [
                        self.pos[0]+x,
                        self.pos[1]+y+1
                    ]

                    collisionChecks.append(collide)    

        for location in collisionChecks:
            # print('LOC',location)
            #check if collider is touching screen floor
            if location[1] > 31:
                return False

            #check for collision with set pixels
            if location in state:
                # print('collide with set pixel')
                return False
            

        return True

    def getLocationOfPixels(self):
        pixels = []
        for y in range(len(self.currentShapeArray)):
            for x in range(len(self.currentShapeArray[y])):
                if self.currentShapeArray[y][x]:
                    pixels.append([x+self.pos[0],y+self.pos[1]])
        # print('pixels',pixels)
        return pixels

    def moveDown(self,canvas,matrix,state):

        if self.locked:
            return

        if not self.canFall(canvas,matrix,state):
            print('cannot fall further')
            self.lockedState = self.getLocationOfPixels()
            self.locked = True
            return
        self.deleteCurrent(canvas,matrix)
        self.pos = [self.pos[0],self.pos[1]+1]
        self.draw(canvas,matrix)
        matrix.SwapOnVSync(canvas)

    def setRotation(self,canvas,matrix,rot):
        self.deleteCurrent(canvas,matrix)
        self.rotation = rot%len(self.rotations)
        self.currentShapeArray = self.rotations[self.rotation]
        self.draw(canvas,matrix)


    def setShape(self,shape):

        shapes = [
            'LPIECE','JPIECE','CUBE','IPIECE',
            'TPIECE','SPIECE','ZPIECE'
        ]

        if shape == 'RANDOM':
            shape = random.choice(shapes)

        if shape == 'LPIECE':
            self.createL() 
        elif shape == 'JPIECE':
            self.createJ() 
        elif shape == 'IPIECE':
            self.createI() 
        elif shape == 'TPIECE':
            self.createT() 
        elif shape == 'SPIECE':
            self.createS() 
        elif shape == 'ZPIECE':
            self.createZ() 
        elif shape == 'CUBE':
            self.createCube() 
        else:
            self.setShape(random.choice(shapes))

    def createS(self):
        self.rotations = [
            [
                [0,1,1],
                [1,1,0],
            ],
            [
                [0,1,0],
                [0,1,1],
                [0,0,1],
            ],
            [
                [0,0,0],
                [0,1,1],
                [1,1,0],
            ],
            [
                [1,0,0],
                [1,1,0],
                [0,1,0],
            ],
        ]
        self.rotation = 0
        self.color = [0,250,0]
        self.currentShapeArray = self.rotations[0]

    def createZ(self):
        self.rotations = [
            [
                [1,1,0],
                [0,1,1],
            ],
            [
                [0,0,1],
                [0,1,1],
                [0,1,0],
            ],
            [
                [0,0,0],
                [1,1,0],
                [0,1,1],
            ],
            [
                [0,1,0],
                [1,1,0],
                [1,0,0],
            ],
        ]
        self.rotation = 0
        self.color = [250,0,0]
        self.currentShapeArray = self.rotations[0]


    def createL(self):
        self.rotations = [
            [
                [0,0,1],
                [1,1,1],
            ],
            [
                [0,1,0],
                [0,1,0],
                [0,1,1]
            ],
            [
                [0,0,0],
                [1,1,1],
                [1,0,0]
            ],
            [
                [1,1,0],
                [0,1,0],
                [0,1,0]
            ]
        ]
        self.rotation = 0
        self.color = [255,165,0]
        self.currentShapeArray = self.rotations[0]

    def createJ(self):
        self.rotations = [
            [
                [1,1,1],
                [0,0,1],
            ],
            [
                [0,1,0],
                [0,1,0],
                [1,1,0]
            ],
            [
                [1,0,0],
                [1,1,1],
                [0,0,0]
            ],
            [
                [0,1,1],
                [0,1,0],
                [0,1,0]
            ]
        ]
        self.rotation = 0
        self.color = [0,0,255]
        self.currentShapeArray = self.rotations[0]

    def createI(self):
        self.rotations = [
            [
                [0,0,0,0],
                [1,1,1,1],
            ],
            [
                [0,1],
                [0,1],
                [0,1],
                [0,1]
            ]
        ]
        self.rotation = 0
        self.color = [137,207,240]
        self.currentShapeArray = self.rotations[0]

    def createT(self):
        self.rotations = [
            [
                [0,1,0],
                [1,1,1],
            ],
            [
                [1,0],
                [1,1],
                [1,0],
            ],
            [
                [1,1,1],
                [0,1,0],
            ],
            [
                [0,1],
                [1,1],
                [0,1],
            ],
        ]
        self.rotation = 0
        self.color = [218,112,214]
        self.currentShapeArray = self.rotations[0]
    
    def createCube(self):
        self.rotations = [
            [
                [1,1],
                [1,1],
            ]
        ]
        self.rotation = 0
        self.color = [255,255,0]
        self.currentShapeArray = self.rotations[0]
    



    # CAN DRAW FLOW:
    # 1 - Calculate next position
    # 2 - Check 'collision map' (parent class? adjacent)
    # 3 - draw
    # 4 - update collision map