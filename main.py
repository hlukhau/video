import cv2
import numpy as np
import time
from ffpyplayer.player import MediaPlayer

p0 = 49, 48
p1 = 679, 236
p2 = 647, 530
p3 = 39, 681

frontCoverPtsAfter = np.array([[0, 0], [1279, 0], [1279, 719], [0, 719]], dtype="float32")
RED = (0, 0, 255)

points = np.array([p0, p1, p2, p3])
frontCoverPtsBefore = np.float32(points[np.newaxis])
print(points)
print(frontCoverPtsBefore)

# Create a VideoCapture object
cap = cv2.VideoCapture('2.mp4')
player = MediaPlayer('2.mp4')

# Check if camera opened successfully
if (cap.isOpened() == False):
    print("Unable to read camera feed")

# Default resolutions of the frame are obtained.The default resolutions are system dependent.
# We convert the resolutions from float to integer.
frame_width = int(cap.get(3))
frame_height = int(cap.get(4))

print(frame_width, frame_height)

# Define the codec and create VideoWriter object.The output is stored in 'outpy.avi' file.
# out = cv2.VideoWriter('out.mp4', cv2.VideoWriter_fourcc(*'MP4V'), 20, (frame_width, frame_height))
out = cv2.VideoWriter('out.mp4', cv2.VideoWriter_fourcc('m', 'p', '4', 'v'), 20, (frame_width, frame_height))

M_front = cv2.getPerspectiveTransform(frontCoverPtsBefore, frontCoverPtsAfter)

# cv2.imshow('img_front', img_front)
# cv2.imshow('frame', frame)
# cv2.waitKey(0)

start_time = time.time()

while (True):
    ret, frame = cap.read()
    audio_frame, val = player.get_frame()

    if ret == True:

        frame = cv2.line(frame, p0, p1, RED, 3)
        frame = cv2.line(frame, p1, p2, RED, 3)
        frame = cv2.line(frame, p2, p3, RED, 3)
        frame = cv2.line(frame, p3, p0, RED, 3)

        frame2 = cv2.warpPerspective(frame, M_front, (1280, 720))

        # Write the frame into the file 'output.avi'
        out.write(frame2)

        # Display the resulting frame
        cv2.imshow('frame', frame)
        cv2.imshow('frame2', frame2)

        if val != 'eof' and audio_frame is not None:
            # audio
            img, t = audio_frame

        # Press Q on keyboard to stop recording
        elapsed = (time.time() - start_time) * 1000  # msec
        play_time = int(cap.get(cv2.CAP_PROP_POS_MSEC))
        sleep = max(1, int(play_time - elapsed))
        if cv2.waitKey(sleep) & 0xFF == ord("q"):
            break

    # Break the loop
    else:
        break

    # When everything done, release the video capture and video write objects
cap.release()
out.release()

# Closes all the frames
cv2.destroyAllWindows()
# url   = "https://www.youtube.com/watch?v=B4zJsDCfpXs"
# video = pafy.new(url)
# best  = video.getbest(preftype="mp4")
# capture = cv2.VideoCapture(best.url)
# while True:
#     check, frame = capture.read()
#     #print (check, frame)
#
#     cv2.imshow('frame', frame)
#     #cv2.waitKey(0)
#
#     if cv2.waitKey(1) == ord('q'):
#         break
#
# capture.release()
# cv2.destroyAllWindows()