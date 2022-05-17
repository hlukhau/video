import zmq
import time

port="5556"
context = zmq.Context()
socket = context.socket(zmq.PUB)
socket.setsockopt(zmq.CONFLATE, 1)
socket.bind("tcp://*:%s" % port)
print ("Running publisher on port: ", port)

while True:
    localtime = time.asctime( time.localtime(time.time()))
    string = "Message published time: {}".format(localtime)
    socket.send_string("{}".format(string))
