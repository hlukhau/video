import cv2
import numpy as np
import time
import os
import logging
from multiprocessing import Process, Value
import base64
import zmq
from zmq import NOBLOCK

path = os.getcwd()
isUnix = False

if (path.find(':') > 0):
    print('Windows OS detected!')
    # from moviepy.editor import *
else:
    isUnix = True
    print('UNIX detected!')

# from pydub.playback import play
# import simpleaudio
# def mp4tomp3(mp4file,mp3file):
#     videoclip=VideoFileClip(mp4file)
#     audioclip=videoclip.audio
#     audioclip.write_audiofile(mp3file)
#     audioclip.close()
#     videoclip.close()


# import os
# import time
# from multiprocessing import Process
# import cv2
#
# def f(display):
#     os.environ['DISPLAY'] = display
#     print(os.environ['DISPLAY'])
#     a = cv2.imread('avatar.png')
#     cv2.imshow('window on %s'%display, a)
#     cv2.waitKey(1000)
#     time.sleep(10)
#
# Process(target=f, args=(':0.0',)).start()
# Process(target=f, args=(':0.1',)).start()



from pydub import AudioSegment
from pydub.playback import _play_with_simpleaudio
from ffpyplayer.player import MediaPlayer

logging.basicConfig(level=logging.INFO)

count = 0


def video_player(displays, run, project):
    video_file = "static/projects/" + project + "/video/video.mp4"
    # print(video_file)

    # if isUnix:
    #     tape = AudioSegment.from_file(video_file, format='mp4')
    #     playback = _play_with_simpleaudio(tape)
    # else:
    if isUnix:
        video_file = path + "/static/projects/" + project + "/video/video.mp4"
    else:
        video_file = path + "\\static\\projects\\" + project + "\\video\\video.mp4"
        # audio_file = path + "\\static\\projects\\" + project + "\\video\\video.mp3"
        # mp4tomp3(video_file, audio_file)
        # player = MediaPlayer(audio_file)
    player = MediaPlayer(video_file)

    count = 0
    before = {}
    after = {}
    M = {}
    widths = {}
    heights = {}
    sockets = {}

    context = zmq.Context()

    for display in displays:
        if display['video'] != True:
            socket = context.socket(zmq.PUB)
            socket.connect('tcp://' + str(display['ip']) + ':' + str(display['port']))
            sockets[display['port']] = socket

            # socket.send_string("hello")
            # response = socket.recv_string()
            #
            # if response == "ok":
            #     print(str(display['port']) + " connected")


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
            frontCoverPtsAfter = np.array([[0, 0], [width - 1, 0], [width - 1, height - 1], [0, height - 1]],
                                          dtype="float32")
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
    # fps = cap.get(cv2.CAP_PROP_FPS)
    # interval = int(1000 / fps)

    fontScale = 1
    color = (255, 255, 255)
    thickness = 2
    font = cv2.FONT_HERSHEY_SIMPLEX

    while (run.value == 1.0):

        ret, frame = cap.read()

        if not isUnix:
            audio_frame, val = player.get_frame()

        if ret == True:

            for display in displays:
                if display['video'] != True:

                    if  display['port'] in sockets:
                        # print("client")
                        port = display['port']
                        # print("port " + str(port))
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

                        frame2 = cv2.putText(frame2, 'FPS: ' + str(round(cap.get(cv2.CAP_PROP_FPS))), (10, 30), font,
                                             fontScale, color, thickness, cv2.LINE_AA)

                        encoded, buffer = cv2.imencode('.jpg', frame2)
                        jpg_as_text = base64.b64encode(buffer)
                        sockets[display['port']].send(jpg_as_text)

                        count = count + 1

                        if count % 30 == 1:
                            for display in displays:
                                if display['video'] != True:
                                    socket = context.socket(zmq.PUB)
                                    socket.connect('tcp://' + str(display['ip']) + ':' + str(display['port']))
                                    sockets[display['port']] = socket

                    # Display the resulting frame
                    # print("port, " + str(width) + " " + str(height))
                    # cv2.imshow(str(port), frame2)
                    # print("after imshow")

            # frame = cv2.putText(frame, 'E: ' + str(round(elapsed)) + ' P: ' + str(round(play_time)) + ' S:' + str(
            #     round(sleep)), (10, 30), font,
            #                      fontScale, color, thickness, cv2.LINE_AA)

            # cv2.imshow('frame', frame)

            # Press Q on keyboard to stop recording
            elapsed = (time.time() - start_time) * 1000  # msec
            cap.set(cv2.CAP_PROP_POS_MSEC, int(elapsed))

            # play_time = int(cap.get(cv2.CAP_PROP_POS_MSEC))
            # sleep = max(1, int(play_time - elapsed))

            if cv2.waitKey(1) & 0xFF == 27:
                break

        # Break the loop
        else:
            break

        if not isUnix:
            if val != 'eof' and audio_frame is not None:
                # windows audio
                img, t = audio_frame

    print('close video player')

    # When everything done, release the video capture and video write objects
    cap.release()

    # Closes all the frames
    cv2.destroyAllWindows()

    # Audio closing
    # if isUnix:
    #     playback.stop()
    # else:
    player.close_player()


    for display in displays:
        if display['video'] != True:

            if display['port'] in sockets:
                sockets[display['port']].close()


if __name__ == '__main__':
    proc1 = Process(target=video_player, args=('video',))
    proc1.start()
    proc1.join()
