"""
CLASS 7 - Python + OpenCV: detect the green color
Goal: Convert each frame to HSV and make a mask of green pixels.

Windows shown:
  1. Original  - what the camera sees
  2. Mask      - white = green detected, black = not green
  3. Highlight - detected green is painted red

Experiment: move the sliders and watch the mask change.
Press 'q' to quit.
"""
import cv2
import numpy as np

cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)
if not cap.isOpened():
    cap = cv2.VideoCapture(0)
if not cap.isOpened():
    print("Webcam not found.")
    raise SystemExit


def nothing(x):
    pass


cv2.namedWindow("Sliders")
cv2.createTrackbar("H low", "Sliders", 35, 179, nothing)
cv2.createTrackbar("H high", "Sliders", 85, 179, nothing)
cv2.createTrackbar("S low", "Sliders", 80, 255, nothing)
cv2.createTrackbar("V low", "Sliders", 50, 255, nothing)

while True:
    ok, frame = cap.read()
    if not ok:
        break

    # Step 1: BGR -> HSV
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    # Step 2: read slider values
    h_low = cv2.getTrackbarPos("H low", "Sliders")
    h_high = cv2.getTrackbarPos("H high", "Sliders")
    s_low = cv2.getTrackbarPos("S low", "Sliders")
    v_low = cv2.getTrackbarPos("V low", "Sliders")

    lower_green = np.array([h_low, s_low, v_low])
    upper_green = np.array([h_high, 255, 255])

    # Step 3: make the mask (white where green)
    mask = cv2.inRange(hsv, lower_green, upper_green)

    # Step 4: paint the green area red so we can see it
    highlight = frame.copy()
    highlight[mask > 0] = (0, 0, 255)

    cv2.imshow("Original", frame)
    cv2.imshow("Mask", mask)
    cv2.imshow("Highlight", highlight)

    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

cap.release()
cv2.destroyAllWindows()
