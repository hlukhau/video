import base64
import cv2
import zmq
import time
import signal
import sys
import logging
logging.basicConfig(level=logging.ERROR)

context = zmq.Context()
footage_socket = context.socket(zmq.PUB)
footage_socket.connect('tcp://localhost:5556')

footage_socket2 = context.socket(zmq.PUB)
footage_socket2.connect('tcp://localhost:5557')

start_time = time.time()
camera = cv2.VideoCapture('3.mp4')  # init the camera
w = int(camera.get(3) / 2)
h = int(camera.get(4) / 2)

print(w, h)

while True:
    grabbed, frame = camera.read()  # grab the current frame
    frame = cv2.resize(frame, (w, h))  # resize the frame
    encoded, buffer = cv2.imencode('.jpg', frame)
    jpg_as_text = base64.b64encode(buffer)
    footage_socket.send(jpg_as_text)
    footage_socket2.send(jpg_as_text)

    elapsed = (time.time() - start_time) * 1000  # msec
    play_time = int(camera.get(cv2.CAP_PROP_POS_MSEC))
    sleep = max(1, int(play_time - elapsed))
    cv2.imshow('server', frame)

    if cv2.waitKey(sleep) & 0xff == 27:
        camera.release()
        cv2.destroyAllWindows()
        break
