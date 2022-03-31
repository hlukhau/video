import cv2
import zmq
import base64
import numpy as np
import sys
import logging

print(sys.argv[1])

logging.basicConfig(level=logging.ERROR)

context = zmq.Context()
receiver = context.socket(zmq.SUB)
receiver.bind('tcp://*:' + sys.argv[1])
receiver.setsockopt_string(zmq.SUBSCRIBE, np.compat.unicode(''))
receiver.setsockopt(zmq.RCVTIMEO, 1000)

while True:
    try:
        frame = receiver.recv_string()
    except:
        break

    img = base64.b64decode(frame)
    npimg = np.frombuffer(img, dtype=np.uint8)
    source = cv2.imdecode(npimg, 1)
    cv2.imshow("Stream", source)

    if cv2.waitKey(1) & 0xff == ord('q'):
        cv2.destroyAllWindows()
        break
