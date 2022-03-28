import cv2
import time
from multiprocessing import Process
import sys
from pydub import AudioSegment
from pydub.playback import play

tape = AudioSegment.from_file('3.mp4', format='mp4')
process = Process(target=play, args=(tape,))


def video(file, process):
    cap = cv2.VideoCapture(file)
    start_time = time.time()


    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break

        cv2.imshow(file, frame)

        elapsed = (time.time() - start_time) * 1000  # msec
        play_time = int(cap.get(cv2.CAP_PROP_POS_MSEC))
        sleep = max(1, int(play_time - elapsed))
        if cv2.waitKey(sleep) & 0xFF == ord("q"):
            break

    cap.release()
    cv2.destroyAllWindows()
    process.terminate()



process.start()

video('3.mp4', process)