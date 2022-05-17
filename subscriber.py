import zmq
import time

port = "5556"
context = zmq.Context()
socket = context.socket(zmq.SUB)

socket.setsockopt_string(zmq.SUBSCRIBE, '')
socket.setsockopt(zmq.CONFLATE, 1)  # last msg only.
socket.connect("tcp://localhost:%s" % port)  # must be placed after above options.

while True:
    data = socket.recv()
    print(data)
    time.sleep(3)
