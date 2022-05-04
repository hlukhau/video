import cv2
import zmq
import base64
import numpy as np
import sys
import logging

print(sys.argv[1])

logging.basicConfig(level=logging.ERROR)


first = 1
waitImage = cv2.imread('static/wait.webp')
cv2.imshow("Start", waitImage)
cv2.waitKey(100)


context = zmq.Context()
receiver = context.socket(zmq.SUB)
receiver.bind('tcp://*:' + sys.argv[1])
receiver.setsockopt_string(zmq.SUBSCRIBE, np.compat.unicode(''))
receiver.setsockopt(zmq.RCVTIMEO, 1000)


while True:
    try:
        frame = receiver.recv_string()
        first = 0
        img = base64.b64decode(frame)
        npimg = np.frombuffer(img, dtype=np.uint8)
        source = cv2.imdecode(npimg, 1)
        # cv2.namedWindow("Stream", cv2.WND_PROP_FULLSCREEN)
        # cv2.setWindowProperty("Stream", cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_AUTOSIZE)
        cv2.imshow("Stream", source)

    except:
        if first == 1:
            cv2.imshow("Start", waitImage)
        else:
            cv2.destroyAllWindows()
            first = 1

    if cv2.waitKey(1) & 0xff == 27:
        cv2.destroyAllWindows()
        break
