import cv2
import numpy as np
import time
import os
import logging
from multiprocessing import Process, Value
# from pydub.playback import play
# import simpleaudio

# from ffpyplayer.player import MediaPlayer

from pydub import AudioSegment
from pydub.playback import _play_with_simpleaudio

import base64
import cv2
import zmq

logging.basicConfig(level=logging.INFO)


# process = Process(target=play, args=(tape,))

def video_player(displays, run):
    # tape = AudioSegment.from_file('3.mp4', format='mp4')
    # playback = _play_with_simpleaudio(tape)

    start_time = time.time()
    before = {}
    after = {}
    M = {}
    widths = {}
    heights = {}

    for display in displays:

        if display['video'] == True:
            x1 = display['points'][0]['x']
            x2 = display['points'][1]['x']
            y1 = display['points'][0]['y']
            y2 = display['points'][2]['y']
            w = x2 - x1
            h = y2 - y1

    for display in displays:
        if display['video'] != True:
            width = float(display['width'])
            height = float(display['height'])

            ps = []

            for point in display['points']:
                ox = float(point['x'])
                oy = float(point['y'])
                x = (ox - x1) * w / width;
                y = (oy - y1) * h / height;
                ps.append([x, y])

            print(width, w)

            frontCoverPtsBefore = np.array(ps, dtype="float32")
            frontCoverPtsAfter = np.array([[0, 0], [width - 1, 0], [width - 1, height - 1], [0, height - 1]], dtype="float32")
            M_front = cv2.getPerspectiveTransform(frontCoverPtsBefore, frontCoverPtsAfter)
            before[display['port']] = frontCoverPtsBefore
            after[display['port']] = frontCoverPtsAfter
            M[display['port']] = M_front
            widths[display['port']] = width
            heights[display['port']] = height


    RED = (0, 0, 255)

    # Create a VideoCapture object
    cap = cv2.VideoCapture('3.mp4')

    if (cap.isOpened() == False):
        print("Unable to read camera feed")

    frame_width = int(cap.get(3))
    frame_height = int(cap.get(4))

    print(frame_width, frame_height)

    while (run.value == 1.0):

        ret, frame = cap.read()
        print("cap.read = " + str(ret))


        if ret == True:

            for display in displays:
                if display['video'] != True:
                    print("client")
                    port = display['port']
                    print("port" + str(port))
                    frontCoverPtsBefore = before[port]
                    frontCoverPtsAfter = after[port]
                    M_front = cv2.getPerspectiveTransform(frontCoverPtsBefore, frontCoverPtsAfter)
                    width = int(widths[port])
                    height = int(heights[port])
                    p0 = int(frontCoverPtsBefore[0][0]), int(frontCoverPtsBefore[0][1])
                    p1 = int(frontCoverPtsBefore[1][0]), int(frontCoverPtsBefore[1][1])
                    p2 = int(frontCoverPtsBefore[2][0]), int(frontCoverPtsBefore[2][1])
                    p3 = int(frontCoverPtsBefore[3][0]), int(frontCoverPtsBefore[3][1])

                    frame = cv2.line(frame, p0, p1, RED, 3)
                    frame = cv2.line(frame, p1, p2, RED, 3)
                    frame = cv2.line(frame, p2, p3, RED, 3)
                    frame = cv2.line(frame, p3, p0, RED, 3)

                    frame2 = cv2.warpPerspective(frame, M_front, (width, height))

                    # Display the resulting frame
                    print("port, " + str(width) + " " + str(height))
                    cv2.imshow(str(port), frame2)
                    print("after imshow")

            cv2.imshow('frame', frame)

            # Press Q on keyboard to stop recording
            elapsed = (time.time() - start_time) * 1000  # msec
            play_time = int(cap.get(cv2.CAP_PROP_POS_MSEC))
            sleep = max(1, int(play_time - elapsed))
            if cv2.waitKey(sleep) & 0xFF == 27:
                break

        # Break the loop
        else:
            break

    print('close video player')

    # When everything done, release the video capture and video write objects
    cap.release()

    # Closes all the frames
    cv2.destroyAllWindows()

    # Audio closing
    print("try to terminate audio process")
    # playback.stop()
    print("after trying of audio process termination")



if __name__ == '__main__':
    proc1 = Process(target=video_player, args=('video',))
    proc1.start()
    proc1.join()

