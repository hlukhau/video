import base64
import cv2
import zmq
import time

context = zmq.Context()
footage_socket = context.socket(zmq.PUB)
footage_socket.connect('tcp://localhost:5555')

start_time = time.time()
camera = cv2.VideoCapture('3.mp4')  # init the camera

while True:
    try:
        grabbed, frame = camera.read()  # grab the current frame
        frame = cv2.resize(frame, (640, 480))  # resize the frame
        encoded, buffer = cv2.imencode('.jpg', frame)
        jpg_as_text = base64.b64encode(buffer)
        footage_socket.send(jpg_as_text)

        elapsed = (time.time() - start_time) * 1000  # msec
        play_time = int(camera.get(cv2.CAP_PROP_POS_MSEC))
        sleep = max(1, int(play_time - elapsed))
        cv2.waitKey(sleep)
        cv2.imshow('server', frame)

    except KeyboardInterrupt:
        camera.release()
        cv2.destroyAllWindows()
        break