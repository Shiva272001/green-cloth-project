"""
CLASS 9 - Final integrated project: Green Cloth - Real-Time Invisible Cloth
Goal: Combine camera + color detection + background replacement, add controls,
      measure FPS, and prepare the final demonstration.

Controls:
  b = capture background (keep cloth out of view, camera still)
  m = show / hide the green mask window
  c = compare: show original and result side by side
  s = save a screenshot (for the testing report)
  q = quit

Testing tip: record FPS and the best HSV values for each lighting condition
(sunlight, tube light, dim light) in your testing report.
"""
import time
import cv2
import numpy as np

# ---------- Settings ----------
CAMERA_INDEX = 0
FRAME_W, FRAME_H = 640, 480
WINDOW = "Green Cloth - Invisible Cloth"

# ---------- Setup ----------
cap = cv2.VideoCapture(CAMERA_INDEX, cv2.CAP_DSHOW)
if not cap.isOpened():
    cap = cv2.VideoCapture(CAMERA_INDEX)
if not cap.isOpened():
    print("Webcam not found.")
    raise SystemExit
cap.set(cv2.CAP_PROP_FRAME_WIDTH, FRAME_W)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, FRAME_H)

kernel = np.ones((3, 3), np.uint8)


def nothing(x):
    pass


cv2.namedWindow("Tuning")
cv2.createTrackbar("H low", "Tuning", 30, 179, nothing)
cv2.createTrackbar("H high", "Tuning", 90, 179, nothing)
cv2.createTrackbar("S low", "Tuning", 30, 255, nothing)
cv2.createTrackbar("V low", "Tuning", 15, 255, nothing)


# ---------- Functions ----------
def capture_background(cap, frames=30):
    print("Capturing background... stay still!")
    collected = []
    for _ in range(frames):
        ok, f = cap.read()
        if ok:
            collected.append(f.astype(np.float32))
    print("Background saved.")
    return np.mean(collected, axis=0).astype(np.uint8)


def make_green_mask(frame):
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    lower = np.array([cv2.getTrackbarPos("H low", "Tuning"),
                      cv2.getTrackbarPos("S low", "Tuning"),
                      cv2.getTrackbarPos("V low", "Tuning")])
    upper = np.array([cv2.getTrackbarPos("H high", "Tuning"), 255, 255])
    mask = cv2.inRange(hsv, lower, upper)
    mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel, iterations=2)
    mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel, iterations=2)
    mask = cv2.dilate(mask, kernel, iterations=1)
    return cv2.GaussianBlur(mask, (5, 5), 0)


def replace_with_background(frame, background, mask):
    m = cv2.merge([mask, mask, mask]).astype(np.float32) / 255.0
    return (background * m + frame * (1 - m)).astype(np.uint8)


# ---------- Main loop ----------
background = None
show_mask = False
compare = False
prev_time = time.time()
fps = 0.0
shot_count = 0

while True:
    ok, frame = cap.read()
    if not ok:
        print("Camera read failed.")
        break

    if background is None:
        output = frame.copy()
        cv2.putText(output, "Press 'b' to capture empty background",
                    (10, 60), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 255), 2)
        mask = None
    else:
        mask = make_green_mask(frame)
        output = replace_with_background(frame, background, mask)

    # FPS calculation (smoothed)
    now = time.time()
    fps = 0.9 * fps + 0.1 * (1.0 / max(now - prev_time, 1e-6))
    prev_time = now
    cv2.putText(output, f"FPS: {fps:.1f}", (10, 30),
                cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)

    # Display
    if compare and background is not None:
        cv2.imshow(WINDOW, np.hstack([frame, output]))
    else:
        cv2.imshow(WINDOW, output)

    if show_mask and mask is not None:
        cv2.imshow("Green Mask", mask)
    elif not show_mask:
        try:
            cv2.destroyWindow("Green Mask")
        except cv2.error:
            pass

    # Keyboard controls
    key = cv2.waitKey(1) & 0xFF
    if key == ord("q"):
        break
    elif key == ord("b"):
        background = capture_background(cap)
    elif key == ord("m"):
        show_mask = not show_mask
    elif key == ord("c"):
        compare = not compare
    elif key == ord("s"):
        shot_count += 1
        name = f"screenshot_{shot_count}.png"
        cv2.imwrite(name, output)
        print("Saved", name)

cap.release()
cv2.destroyAllWindows()
