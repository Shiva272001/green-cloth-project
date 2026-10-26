"""
CLASS 8 - Background replacement (the invisible effect)
Goal: Save the empty background, then replace green pixels with it.

Controls:
  b = capture background (stand out of the frame, keep the cloth OUT of view!)
  q = quit

Steps for the demo:
  1. Point the camera at the empty scene. Press 'b'. Wait for it to finish.
  2. Bring the green cloth into view. The cloth should look invisible.
Keep the camera still after pressing 'b'.
"""
import cv2
import numpy as np

cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)
if not cap.isOpened():
    cap = cv2.VideoCapture(0)
if not cap.isOpened():
    print("Webcam not found.")
    raise SystemExit

background = None
kernel = np.ones((3, 3), np.uint8)

# Tuned green range to catch dark green cloth, folds, and shadows
LOWER_GREEN = np.array([30, 30, 15])
UPPER_GREEN = np.array([90, 255, 255])


def capture_background(cap, frames=30):
    """Take 30 frames and average them to reduce camera noise."""
    print("Capturing background... stay still!")
    collected = []
    for _ in range(frames):
        ok, f = cap.read()
        if ok:
            collected.append(f.astype(np.float32))
    print("Background saved.")
    return np.mean(collected, axis=0).astype(np.uint8)


while True:
    ok, frame = cap.read()
    if not ok:
        break

    if background is None:
        msg = "Press 'b' to capture the empty background"
        cv2.putText(frame, msg, (10, 30), cv2.FONT_HERSHEY_SIMPLEX,
                    0.7, (0, 255, 255), 2)
        cv2.imshow("Class 8 - Invisible Cloth", frame)
    else:
        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        mask = cv2.inRange(hsv, LOWER_GREEN, UPPER_GREEN)

        # Clean the mask: remove tiny dots, fill small holes, soften edges
        mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel, iterations=2)
        mask = cv2.dilate(mask, kernel, iterations=1)
        mask = cv2.GaussianBlur(mask, (5, 5), 0)

        # Where mask is white -> take pixel from background, else from camera
        mask_3ch = cv2.merge([mask, mask, mask]).astype(np.float32) / 255.0
        result = (background * mask_3ch + frame * (1 - mask_3ch)).astype(np.uint8)

        cv2.imshow("Class 8 - Invisible Cloth", result)

    key = cv2.waitKey(1) & 0xFF
    if key == ord("b"):
        background = capture_background(cap)
    elif key == ord("q"):
        break

cap.release()
cv2.destroyAllWindows()
