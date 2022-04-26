import cv2
import numpy as np
import time
import os
import logging
from multiprocessing import Process, current_process
from pydub import AudioSegment
from pydub.playback import play

logging.basicConfig(level=logging.ERROR)

start_time = time.time()

tape = AudioSegment.from_file('3.mp4', format='mp4')
process = Process(target=play, args=(tape,))


def video_player(name, frontCoverPtsAfter, frontCoverPtsBefore, width, height):
    print(name)
    RED = (0, 0, 255)
    # p0 = 49, 48
    # p1 = 679, 236
    # p2 = 647, 530
    # p3 = 39, 681
    #
    # frontCoverPtsAfter = np.array([[0, 0], [1279, 0], [1279, 719], [0, 719]], dtype="float32")
    #
    # frontCoverPtsBefore = np.array([p0, p1, p2, p3], dtype="float32")
    # print(frontCoverPtsBefore)
    p0 = int(frontCoverPtsBefore[0][0]), int(frontCoverPtsBefore[0][1])
    p1 = int(frontCoverPtsBefore[1][0]), int(frontCoverPtsBefore[1][1])
    p2 = int(frontCoverPtsBefore[2][0]), int(frontCoverPtsBefore[2][1])
    p3 = int(frontCoverPtsBefore[3][0]), int(frontCoverPtsBefore[3][1])

    print(p0, p1, p2, p3)

    M_front = cv2.getPerspectiveTransform(frontCoverPtsBefore, frontCoverPtsAfter)

    # Create a VideoCapture object
    cap = cv2.VideoCapture('3.mp4')

    if (cap.isOpened() == False):
        print("Unable to read camera feed")

    frame_width = int(cap.get(3))
    frame_height = int(cap.get(4))

    print(M_front, width, height)

    print(frame_width, frame_height)

    while (True):
        ret, frame = cap.read()

        if ret == True:

            frame = cv2.line(frame, p0, p1, RED, 3)
            frame = cv2.line(frame, p1, p2, RED, 3)
            frame = cv2.line(frame, p2, p3, RED, 3)
            frame = cv2.line(frame, p3, p0, RED, 3)

            frame2 = cv2.warpPerspective(frame, M_front, (width, height))

            # Display the resulting frame
            #cv2.imshow('frame', frame)
            cv2.imshow(name, frame2)


            # Press Q on keyboard to stop recording
            elapsed = (time.time() - start_time) * 1000  # msec
            play_time = int(cap.get(cv2.CAP_PROP_POS_MSEC))
            sleep = max(1, int(play_time - elapsed))
            if cv2.waitKey(sleep) & 0xFF == ord("q"):
                break

        # Break the loop
        else:
            break

    print('close video player')

    # When everything done, release the video capture and video write objects
    cap.release()

    # Closes all the frames
    cv2.destroyAllWindows()





if __name__ == '__main__':
    proc1 = Process(target=video_player, args=('video',))
    proc1.start()
    proc1.join()

