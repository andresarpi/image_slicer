# USAGE
# python opencv_object_tracking.py
# python opencv_object_tracking.py --video dashcam_boston.mp4 --tracker csrt

# import the necessary packages
from imutils.video import VideoStream
from imutils.video import FPS
import argparse
import imutils
import time
import cv2

# construct the argument parser and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("-v", "--video", type=str, default="../videos/farmacia.mp4",
	help="path to input video file")
ap.add_argument("-g", "--gap", type=int, default=50,
	help="gap in between frames")

args = vars(ap.parse_args())

# extract the OpenCV version info
(major, minor) = cv2.__version__.split(".")[:2]

try:
    cap = cv2.VideoCapture(args["video"])
except:
    print("Couldnt open video file. Closing...")
    exit()

frame = None
gap = args["gap"]
first_point = None
second_click = False
point = (0,0)
counter = -1

def handle_selection(pt1, pt2):
    global frame

    cv2.rectangle(frame, pt1, pt2,(0,255,0), 1)
    cv2.imshow("Frame", frame)

def mouse_drawing(event, x, y, flags, params):
    global point, second_click, first_point
    if event == cv2.EVENT_LBUTTONDOWN:
        point = (x, y)

        if (second_click):
            handle_selection(first_point, point)
        else:
            first_point = point

        second_click = not second_click
        

cv2.namedWindow("Frame")
cv2.setMouseCallback("Frame", mouse_drawing)

while True:
    found, frame = cap.read()
    if not found:
        break

    counter += 1
    if (counter % gap != 0):
        
        second_click = False
        continue

    cv2.imshow("Frame", frame)
    key = cv2.waitKey(0)


cap.release()
cv2.destroyAllWindows()