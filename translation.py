import cv2
import numpy as np
import time
import os
import logging
from multiprocessing import Process, Value
import base64
import zmq

path = os.getcwd()
isUnix = False

if (path.find(':') > 0):
    print('Windows OS detected!')

else:
    isUnix = True
    print('UNIX detected!')
    from pydub import AudioSegment
    from pydub.playback import play


# from pydub.playback import play
# import simpleaudio

# from ffpyplayer.player import MediaPlayer
from pydub import AudioSegment
from pydub.playback import _play_with_simpleaudio


logging.basicConfig(level=logging.INFO)


# process = Process(target=play, args=(tape,))

def video_player(displays, run, project):

    video_file = "static/projects/" + project + "/video/video.mp4"
    # print(video_file)

    if (isUnix):
        tape = AudioSegment.from_file(video_file, format='mp4')
        playback = _play_with_simpleaudio(tape)

    before = {}
    after = {}
    M = {}
    widths = {}
    heights = {}
    sockets = {}

    context = zmq.Context()

    for display in displays:
        if display['video'] != True:
            sockets[display['port']] = context.socket(zmq.PUB)
            sockets[display['port']].connect('tcp://localhost:' + str(display['port']))
            print('Socket on port' + str(display['port']) + ' connected')


    for display in displays:
        if display['video'] == True:
            x1 = display['points'][0]['x']
            x2 = display['points'][1]['x']
            y1 = display['points'][0]['y']
            y2 = display['points'][2]['y']
            w = x2 - x1
            h = y2 - y1
            # print('video w=' + str(w) + ' h=' + str(h))
            video_width = float(display['width'])
            video_height = float(display['height'])

    for display in displays:
        if display['video'] != True:
            width = float(display['width'])
            height = float(display['height'])

            ps = []

            for point in display['points']:
                ox = float(point['x'])
                oy = float(point['y'])
                x = (ox - x1) * video_width / w;
                y = (oy - y1) * video_height / h;
                ps.append([x, y])

            # print(width, w)

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
    cap = cv2.VideoCapture(video_file)

    if (cap.isOpened() == False):
        print("Unable to read camera feed")

    frame_width = int(cap.get(3))
    frame_height = int(cap.get(4))

    # print(frame_width, frame_height)
    start_time = time.time()
    elapsed = 0
    play_time = 0
    sleep = 0
    fps = cap.get(cv2.CAP_PROP_FPS)
    interval = int(1000 / fps)

    while (run.value == 1.0):

        ret, frame = cap.read()
        # print("cap.read = " + str(ret))


        if ret == True:

            for display in displays:
                if display['video'] != True:
                    # print("client")
                    port = display['port']
                    # print("port" + str(port))
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

                    fontScale = 1
                    color = (255, 255, 255)
                    thickness = 2
                    font = cv2.FONT_HERSHEY_SIMPLEX
                    frame2 = cv2.putText(frame2, 'E: ' + str(round(elapsed)) + ' P: ' + str(round(play_time)) + ' S:' + str(round(sleep)), (10, 30), font,
                                        fontScale, color, thickness, cv2.LINE_AA)

                    encoded, buffer = cv2.imencode('.jpg', frame2)
                    jpg_as_text = base64.b64encode(buffer)
                    sockets[display['port']].send(jpg_as_text)
                    # Display the resulting frame
                    # print("port, " + str(width) + " " + str(height))
                    # cv2.imshow(str(port), frame2)
                    # print("after imshow")

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

