from buildhat import Motor, ColorSensor, ForceSensor
import kociemba  # for custom event to solve cubes
from math import *
import os, struct, time


# constants
flipperMotor = Motor('D')
flipperHome = 12
flipperHold = 143
flipperFlip = 274 - 360
flipperScanEdge = 198 - 360
flipperScanCenter = 243 - 360
flipperScanCorner = 184 - 360
flipperSpin = 43

rotaterMotor = Motor('C')
rotaterHome = 0

button = ForceSensor('B')

# Enums (spike prime doesnt support enum library)
# turn direction
prime = 1
regular = 2

colorTable = ['white', 'red', 'green', 'yellow', 'orange', 'blue']
faceTable = ['U', 'R','F','D','L','B']

class Face():
    U = 0
    R = 1
    F = 2
    D = 3
    L = 4
    B = 5

# calibration data
colorReference = [None] * 6
calibrationFile = os.path.expanduser("~/cubecolors")

# load color reference
colorReference = [None] * 6
#if os.path.isfile('data/cubecolors'):
try:
    with open(calibrationFile, 'rb') as file:
        print("Reading calibration file")
        for face in range(6):
            colorReference[face] = struct.unpack('4I', file.read(16))
            file.close
except:
    print("No calibration data.  please calibrate the cube.")

scaner = ColorSensor('A')
#color values go here 

#pos = motor.get_position()
#print("hello {}".format(pos))


# Functions
def Initialize():
    # setting the home state for the two motors
    flipperMotor.release = False
    rotaterMotor.release = False
    flipperMotor.set_default_speed(20)
    rotaterMotor.set_default_speed(20)
    flipperMotor.run_to_position(flipperHome, direction="anticlockwise")
    rotaterMotor.run_to_position(rotaterHome)


def Solved():
    # what will happon when the cube is solved 
    flipperMotor.run_to_position(flipperHome, direction="anticlockwise")
    rotaterMotor.run_for_degrees(0)
    # add fun stuff 


def turnD(count, direction = regular): 
    # turning the D layer on the cube
    flipperMotor.run_to_position(flipperHold)
    internal_rotateY(count, direction)

def rotateY(count, direction = regular):
    # rotating the cube on the y-axis
    if flipperMotor.get_position()-20 < flipperHold and flipperMotor.get_position()+20 > flipperHold:
        flipperMotor.run_to_position(flipperSpin, direction="anticlockwise" )
     
    if direction == regular :
        rotaterMotor.run_for_degrees(90 * count)
    else:
        rotaterMotor.run_for_degrees(-90 * count)
    

def internal_rotateY(count, direction = regular):
    # alowing the cube carier to turn the cube
    if direction == regular :
        rotaterMotor.run_for_degrees(-90 * count)
    else:
        rotaterMotor.run_for_degrees(90 * count)

def flipX(count):
    # fliping the cube on the x-axis 
    for x in range(count):
        flipperMotor.run_to_position(flipperHold)
        time.sleep(.3) 
        flipperMotor.run_to_position(flipperFlip)  
        time.sleep(.5) 

def calibrate():
    # the motion to calibrate the colors 
    flipperMotor.run_to_position(flipperHold)
    flipX(1)
    calibrateCenter(Face.U)
    flipX(1)
    calibrateCenter(Face.F)
    flipX(1)
    calibrateCenter(Face.D)
    flipX(1)
    calibrateCenter(Face.B)
    rotateY(1)
    flipX(1)
    calibrateCenter(Face.R)
    flipX(2)
    calibrateCenter(Face.L)
    rotateY(1, prime)
    flipX(1)
    rotateY(1, prime)
    # save color reference
    with open(calibrationFile,'wb')as file:
        for rgb in colorReference:
            file.write(struct.pack('4I',*rgb))
    file.close
    
def calibrateCenter(face):
    # scaning the centers to compair the color to other peices 
    flipperMotor.run_to_position(flipperScanCenter)
    time.sleep(0.5)
    rgb = scaner.get_color_rgbi()
    colorReference[face] = rgb
    print('{} center {}R {}G {}B {}I'.format(face,rgb[0],rgb[1],rgb[2],rgb[3]))


def getSide(rgb):
    bestSide = -1
    bestSideE = 100000000000
    # loop all the calibrarion colors and return the index of the closest one
    for currentSide in range(6):
        refRgb = colorReference[currentSide]
        # fancy math
        eTotal = colorDistance(rgb, refRgb)
        # er = abs (rgb[0] - refRgb[0])
        # eg = abs (rgb[1] - refRgb[1])
        # eb = abs (rgb[2] - refRgb[2])
        # eTotal = er + eg + eb
        # may need to inprove this compairison 
        if eTotal < bestSideE:
            bestSide = currentSide
            bestSideE = eTotal
    return bestSide 

#             |************|
#             |*U1**U2**U3*|
#             |************|
#             |*U4**U5**U6*|
#             |************|
#             |*U7**U8**U9*|
# ____________|************|_________________________
# ************|************|************|************|
# *L1**L2**L3*|*F1**F2**F3*|*R1**R2**R3*|*B1**B2**B3*|
# ************|************|************|************|
# *L4**L5**L6*|*F4**F5**F6*|*R4**R5**R6*|*B4**B5**B6*|
# ************|************|************|************|
# *L7**L8**L9*|*F7**F8**F9*|*R7**R8**R9*|*B7**B8**B9*|
# ************|************|************|************|
# ------------|************|-------------------------
#             |*D1**D2**D3*|
#             |************|
#             |*D4**D5**D6*|
#             |************|
#             |*D7**D8**D9*|
#             |************|


scanResult = [None] * (6 * 9)
scanColorResult = [[None]*9] * 6

def scanCube():
    # scaning the whole cube
    flipperMotor.run_to_position(flipperHold)
    flipX(1)
    scanFace(Face.U)
    flipX(1)
    scanFace(Face.F)
    flipX(1)
    scanFace(Face.D)
    flipX(1)
    rotateY(2)
    scanFace(Face.B)
    rotateY(1, prime)
    flipX(1)
    rotateY(1)
    scanFace(Face.R)
    flipX(2)
    rotateY(2)
    scanFace(Face.L)
    # puttting the cube back in the right orentation 
    rotateY(2)
    flipX(1)
    rotateY(1, prime)
    cubeString = ''.join(scanResult)
    print("cubestring = %s" % cubeString)
    for i in range(6):
        print("{} = {}".format(faceTable[i], ' '.join(scanColorResult[i])))

    # send the cube state to the raspberry pi to be solved
    return cubeString

def scanFace(face):
    # center
    flipperMotor.run_to_position(flipperScanCenter)
    scanTile(face, 5)

    # scan the tiles
    position = 0
    rotaterMotor.run_to_position(position)
    tiles = [8,9,6,3,2,1,4,7]
    for tileIndex in range(8):
        if (tileIndex % 2 == 1): # odd number must be a corner
            flipperMotor.run_to_position(flipperScanCorner)
        else:
            flipperMotor.run_to_position(flipperScanEdge)
        scanTile(face, tiles[tileIndex])
        position += 45
        angle = position if position <= 180 else position - 360
        print("{} - {}".format(position, angle))
        rotaterMotor.run_to_position(angle)
    time.sleep(0.3)

def scanTile(face, tile):
    # stating the location and color
    rgb = scaner.get_color_rgbi()
    color = getSide(rgb)
    scanResult[(face*9) + tile - 1] = faceTable[color]
    scanColorResult[face][tile - 1] = colorTable[color] # for debugging
    print("{}-{} color is {}".format(faceTable[face], tile, colorTable[color]))

#  UUUUUUUUU RRRFRRRRR FLFFFFFFF DDDDDDDDD LLLRLLLLL BBBBBBBBB

def uMove(count, direction = regular):
    flipX(2)
    turnD(count, direction)
    flipX(2)
    
def fMove(count, direction = regular):
    rotateY(2)
    flipX(1)
    turnD(count, direction)
    rotateY(2)
    flipX(1)

def bMove(count, direction = regular):
    flipX(1)
    turnD(count, direction)
    flipX(3)

def rMove(count, direction = regular):
    rotateY(1, prime)
    flipX(1)
    turnD(count, direction)
    rotateY(2)
    flipX(1)
    rotateY(1, prime)

def lMove(count, direction = regular):
    rotateY(1)
    flipX(1)
    turnD(count, direction)
    rotateY(2)
    flipX(1)
    rotateY(1)

def dMove(count, direction = regular):
    turnD(count, direction)


def solveCube(solution: str):
    print("solving cube with moves: %s" % solution)
    moves = solution.split(' ')
    for move in moves:
        print("Executing move: %s" % move)
        face = move[0]
        count = 1
        direction = regular
        if len(move) == 2:
            if move[1] == "2":
                count = 2
            elif move[1] == "'":
                direction = prime
        # call the move function dynamicly using a nameing convention see https://www.danielmorell.com/blog/dynamically-calling-functions-in-python-safely
        globals()["{}Move".format(face.lower())](count, direction)


# compute distance between two colors.  see https://stackoverflow.com/questions/54242194/python-find-the-closest-color-to-a-color-from-giving-list-of-colors
def colorDistance(rgbi1, rgb2):
    r, g, b, i = rgbi1
    cr, cg, cb, ib = rgb2
    # pythagorean theorem
    return sqrt((r - cr)**2 + (g - cg)**2 + (b - cb)**2 + (i - ib)**2)


# in case we need super fancy math
# convert rgb to CIELAB color space. see https://en.wikipedia.org/wiki/CIELAB_color_space
def rgb2lab ( inputColor ) :

   num = 0
   RGB = [0, 0, 0]

   for value in inputColor :
       value = float(value) / 255

       if value > 0.04045 :
           value = ( ( value + 0.055 ) / 1.055 ) ** 2.4
       else :
           value = value / 12.92

       RGB[num] = value * 100
       num = num + 1

   XYZ = [0, 0, 0,]

   X = RGB [0] * 0.4124 + RGB [1] * 0.3576 + RGB [2] * 0.1805
   Y = RGB [0] * 0.2126 + RGB [1] * 0.7152 + RGB [2] * 0.0722
   Z = RGB [0] * 0.0193 + RGB [1] * 0.1192 + RGB [2] * 0.9505
   XYZ[ 0 ] = round( X, 4 )
   XYZ[ 1 ] = round( Y, 4 )
   XYZ[ 2 ] = round( Z, 4 )

   XYZ[ 0 ] = float( XYZ[ 0 ] ) / 95.047         # ref_X =  95.047   Observer= 2°, Illuminant= D65
   XYZ[ 1 ] = float( XYZ[ 1 ] ) / 100.0          # ref_Y = 100.000
   XYZ[ 2 ] = float( XYZ[ 2 ] ) / 108.883        # ref_Z = 108.883

   num = 0
   for value in XYZ :

       if value > 0.008856 :
           value = value ** ( 0.3333333333333333 )
       else :
           value = ( 7.787 * value ) + ( 16 / 116 )

       XYZ[num] = value
       num = num + 1

   Lab = [0, 0, 0]

   L = ( 116 * XYZ[ 1 ] ) - 16
   a = 500 * ( XYZ[ 0 ] - XYZ[ 1 ] )
   b = 200 * ( XYZ[ 1 ] - XYZ[ 2 ] )

   Lab [ 0 ] = round( L, 4 )
   Lab [ 1 ] = round( a, 4 )
   Lab [ 2 ] = round( b, 4 )

   return Lab

# main program
Initialize()

# wait for scramble and input


# tests
# calibrate()
cube = scanCube()
solution = kociemba.solve(cube)
solveCube(solution)



# print("Solving %s" % solution)
# m.run_for_rotations(-.1, 50)

# lMove(1)
# bMove(1, prime)
# dMove(1)
# rMove(2)
# bMove(1)
# lMove(1, prime)
# bMove(2)
# lMove(1)
# bMove(1, prime)
# lMove(2)
# dMove(2)
# bMove(2)
# rMove(2)
# bMove(1, prime)
# dMove(2)
# lMove(2)
# bMove(1, prime)
# uMove(2)
# dMove(2)
# lMove(1,prime)



#colorReference = [(49,13,99), (600,346,200), (50,500,50), (80,660,570), (6,760,50), (51,15,101)]
#print("1 best side is {}".format(getSide((50,14,100))))
#print("2 best side is {}".format(getSide((50,14,287))))
#print("3 best side is {}".format(getSide((789,660,570))))
#calibrate()
#turnD(1, regular)
#flipX(2)
#rotateY(2, prime)
#turnD(1, prime)
#rotateY(1)
#flipX(1)
#turnD(2)
#turnD(1)
#scanCube()

Solved()
