#!/usr/bin/env python3

import base64, re, os, signal, time, argparse
import kociemba  # for custom event to solve cubes
from spike_rpc import RPC

# constants for the status mesage
MOTOR_TYPES = [65, 48, 49, 75, 76, 38, 46, 47]
SPIKE_COLOR = 61
PORTS_NAMES = ['A','B','C','D','E','F']

# Argument parsing
parser = argparse.ArgumentParser(description='Upload, run, and monitor a Lego Spike python program')
parser.add_argument('-p', '--port', help='Spike Hub device path or com port', default='/dev/ttyACM0')
parser.add_argument('-f', '--filename', help='Program to run')
parser.add_argument('-s', '--slot', help='Slot of the program to run', type=int, default=0)
parser.add_argument('-t', '--type', help='Type of Spike application',choices=("python", "scratch"), default="python")
parser.add_argument('-m', '--monitor', help='Monitor device status information', action=argparse.BooleanOptionalAction)
parser.add_argument('--debug', help='Enable debug', action='store_true')
args = parser.parse_args()
if args.debug:
    logging.basicConfig(level=logging.DEBUG)

# upload and run the program
rpc = RPC(args.port)
spikeFile = os.path.abspath(args.filename)
rpc.uploadProgram(spikeFile, args.slot, args.type)
rpc.program_execute(args.slot)

# if we ctrl+C then stop the running program
def handler(signum, frame):
    rpc.program_terminate()
    exit(0)
signal.signal(signal.SIGINT, handler)

show_status = args.monitor

start = time.time()
# read the output
while (True):

    # read messages from the spike
    msg = rpc.getNextMessage()
    # handle RPC events
    if msg and isinstance(msg, dict):
        # messages
        if 'm' in msg:
            # when a cube is scanned then create a solution and send it back
            if msg['m'] == 'cube_scanned':
                cube = msg['p']
                print("Recieved scanned cube %s" % cube)
                solution = kociemba.solve(cube)
                print("Sending cube solution %s" % solution)
                rpc.send_message("solve_cube", solution, False)

            # handle errors
            elif msg['m'] == 'user_program_error' or msg['m'] == 'runtime_error':
                error = base64.b64decode(msg['p'][3]).decode('utf-8')
                # make source file links clickable in VSCode by updating the path to be the local file
                error = re.sub("\./projects/\d+/__init__.py", spikeFile, error)
                print('\033[91m' + error + '\033[0m')

            # program start stop messages
            elif msg['m'] == 12:
                if msg['p'][1]:
                    print("Program started")
                else:
                    print("Program ended")
                    break # end monitoring
            
            # handle device status messages
            elif msg['m'] == 0:
                if show_status:
                    status = msg['p']
                    statusOut = ""
                    for i in range(6):
                        if status[i][0] in MOTOR_TYPES:
                            statusOut += "{}:motor({:>4},{:>4}) ".format(PORTS_NAMES[i], status[i][1][1], status[i][1][2])
                        elif status[i][0] == SPIKE_COLOR:
                            statusOut += "{}:color({:>3},{:>3},{:>3}) ".format(PORTS_NAMES[i], status[i][1][2], status[i][1][3], status[i][1][4])
                    if statusOut:
                        print(statusOut)

            # battery  [8.294, 100, True]
            elif msg['m'] == 2:
                if show_status:
                    print("Battery: {}%".format(msg['p'][1]))

            # print any unknown messages
            else:
                print(repr(msg))
        
        # system errors
        elif 'e' in msg:
            error = base64.b64decode(msg['e']).decode('utf-8')
            print('\033[91m' + error + '\033[0m')

        # print unknown json object
        elif msg:
            print(repr(msg))

    # print any strings output via 'print' in the program
    elif msg:
        if msg == "exit":
            rpc.program_terminate()
            exit(0)
        print(msg)
