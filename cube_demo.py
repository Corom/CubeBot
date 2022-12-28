print("hello")

from protocol.ujsonrpc import json_rpc
from spike.control import wait_for_seconds
from spike import Motor
m = Motor('C')

state = dict()
def recieve_solution(p, id):
  print("Recieved solution to cube %s" % p)
  # store the solution in a state dictionary that we are waiting for
  state['solution'] = p

# register the custom message handler for solve_cube
json_rpc.add_method("solve_cube", recieve_solution)

for i in range(3):
  # send a scanned
  m.run_for_rotations(.1, 50)
  print("sending scanned cube result")
  json_rpc.emit("cube_scanned", 'DRLUUBFBRBLURRLRUBLRDDFDLFUFUFFDBRDUBRUFLLFDDBFLUBLRBD')

  print("Waiting for solution")
  while('solution' not in state):
    wait_for_seconds(.1)

  # get the solution and delete it
  solution = state['solution']
  del state['solution']

  print("Solving %s" % solution)
  m.run_for_rotations(-.1, 50)


print ("all done")
json_rpc.emit(12, ("", False))  # regular python programs dont actually exit. This tells the system that the program is done
