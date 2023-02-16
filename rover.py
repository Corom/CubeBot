from buildhat import *

pair = MotorPair('A', 'B')
pair._left  motor
color = ColorSensor('D')
dist = DistanceSensor('C')

pair.set_default_speed(100)
pair.run_for_rotations(2)


#pair.run_for_rotations(1, speedl=100, speedr=20)

pair.run_to_position(20, 100, speed=20)