import cv2
import zmq
import base64
import numpy as np
import sys
import logging

port = ''
fullscreen = 'no'
offset = 0

try:
    port = sys.argv[1]
    fullscreen = int(sys.argv[2])
    offset = int(sys.argv[3])
except:
    offset = 0


def listen(port, fullscreen, offset):
    logging.basicConfig(level=logging.ERROR)

    first = 1
    waitImage = cv2.imread('static/wait.webp')


    print('Starting client proceess at ' + str(port) + ' port')

    name_stream = "Stream:" + port
    name_waiting = "Listening:" + port

    context = zmq.Context()
    receiver = context.socket(zmq.SUB)
    receiver.setsockopt_string(zmq.SUBSCRIBE, np.compat.unicode(''))
    receiver.setsockopt(zmq.CONFLATE, 1)  # last msg only.
    receiver.setsockopt(zmq.RCVTIMEO, 1000)
    receiver.bind('tcp://*:' + port)

    cv2.imshow(name_waiting, waitImage)

    while True:
        try:
            frame = receiver.recv_string()

            if first == 1:
                position = cv2.getWindowImageRect(name_waiting)
                cv2.destroyWindow(name_waiting)

            first = 0
            img = base64.b64decode(frame)
            npimg = np.frombuffer(img, dtype=np.uint8)
            source = cv2.imdecode(npimg, 1)

            if fullscreen == 1:
                cv2.namedWindow(name_stream, cv2.WND_PROP_FULLSCREEN)
                cv2.setWindowProperty(name_stream, cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_AUTOSIZE)

            cv2.imshow(name_stream, source)

            if fullscreen == 1:
                cv2.moveWindow(name_stream, offset, 0)
        except:
            if first == 0:
                cv2.destroyWindow(name_stream)
                cv2.imshow(name_waiting, waitImage)
                cv2.moveWindow(name_waiting, position[0], position[1])
                first = 1

        if cv2.waitKey(1) & 0xff == 27:
            cv2.destroyAllWindows()
            break


listen(port, fullscreen, offset)