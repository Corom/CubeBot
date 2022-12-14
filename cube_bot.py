from spike import PrimeHub, LightMatrix, Button, StatusLight, ForceSensor, MotionSensor, Speaker, ColorSensor, App, DistanceSensor, Motor, MotorPair
from spike.control import wait_for_seconds
from spike import ColorSensor
from math import *
import uos, ustruct


# constants
hub = PrimeHub()
flipperMotor = Motor('C')
flipperHome = 12
flipperHold = 143
flipperFlip = 274
flipperScanEdge = 198
flipperScanCenter = 243
flipperScanCorner = 184
flipperSpin = 43

rotaterMotor = Motor('A')
rotaterHome = 0

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
calibrationFile = "/data/cubecolors"

# load color reference
colorReference = [None] * 6
#if uos.path.isfile('data/cubecolors'):
try:
    with open(calibrationFile, 'rb') as file:
        print("Reading calibration file")
        for face in range(6):
            colorReference[face] = ustruct.unpack('3I', file.read(12))
            file.close
except:
    print("No calibration data.  please calibrate the cube.")

scaner = ColorSensor('E')
#color values go here 

#pos = motor.get_position()
#print("hello {}".format(pos))

hub = PrimeHub()

# Functions
def Initialize():
    # setting the home state for the two motors 
    flipperMotor.set_stop_action("hold")
    rotaterMotor.set_stop_action("hold")
    flipperMotor.run_to_position(flipperHome, "counterclockwise")
    rotaterMotor.run_to_position(rotaterHome)


def Solved():
    # what will happon when the cube is solved 
    flipperMotor.run_to_position(flipperHome, "counterclockwise")
    # add fun stuff 


def turnD(count, direction = regular): 
    # turning the D layer on the cube
    flipperMotor.run_to_position(flipperHold)
    internal_rotateY(count, direction)

def rotateY(count, direction = regular):
    # rotating the cube on the y-axis
    flipperMotor.run_to_position(flipperSpin, "counterclockwise" )
    internal_rotateY(count, direction)

def internal_rotateY(count, direction = regular):
    # alowing the cube carier to turn the cube
    if direction == regular :
        rotaterMotor.run_for_degrees(90 * count)
    else:
        rotaterMotor.run_for_degrees(-90 * count)

def flipX(count):
    # fliping the cube on the x-axis 
    for x in range(count):
        flipperMotor.run_to_position(flipperHold)
        flipperMotor.run_to_position(flipperFlip)        

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
    try:
        uos.mkdir("data")
    except:
        print("data directory already exists")
    with open(calibrationFile,'wb')as file:
        for rgb in colorReference:
            file.write(ustruct.pack('3I',*rgb))
    file.close
    
def calibrateCenter(face):
    # scaning the centers to compair the color to other peices 
    flipperMotor.run_to_position(flipperScanCenter)
    wait_for_seconds(0.5)
    rgb = scaner.get_rgb_intensity()
    colorReference[face] = rgb
    print('{} center {}R {}G {}B'.format(face,rgb[0],rgb[1],rgb[2]))


def getSide(rgb):
    bestSide = -1
    bestSideE = 100000000000
    # loop all the calibrarion colors and return the index of the closest one
    for currentSide in range(6):
        refRgb = colorReference[currentSide]
        er = abs (rgb[0] - refRgb[0])
        eg = abs (rgb[1] - refRgb[1])
        eb = abs (rgb[2] - refRgb[2])
        eTotal = er + eg + eb
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
    scanFace(Face.B)
    rotateY(1)
    flipX(1)
    scanFace(Face.R)
    flipX(2)
    scanFace(Face.L)
    # puttting the cube back in the right orentation 
    rotateY(1, prime)
    flipX(1)
    rotateY(1, prime)

def scanFace(face):
    # center
    flipperMotor.run_to_position(flipperScanCenter)
    scanTile(face, 5)

    # scan the tiles
    tiles = [8,9,6,3,2,1,4,7]
    for tileIndex in range(8):
        if (tileIndex % 2 == 1): # odd number must be a corner
            flipperMotor.run_to_position(flipperScanCorner)
        else:
            flipperMotor.run_to_position(flipperScanEdge)
        scanTile(face, tiles[tileIndex])
        rotaterMotor.run_for_degrees(45)
    wait_for_seconds(0.3)

def scanTile(face, tile):
    # stating the location and color
    rgb = scaner.get_rgb_intensity()
    color = getSide(rgb)
    print("{}-{} color is {}".format(faceTable[face], tile, colorTable[color]))

    


# main program
Initialize()

# wait for scramble and input

# tests

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
scanCube()

Solved()