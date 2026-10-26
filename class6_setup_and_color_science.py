"""
CLASS 6 - Physical setup and color science
Goal: Show the live webcam feed and learn how a color looks to the computer.

How to use:
  - Click anywhere on the video to see that pixel's BGR and HSV values.
  - Click on the green cloth, then change the room lighting and click again.
    Notice how the numbers change. This is why lighting matters!
  - Press 'q' to quit.

Install first:  pip install opencv-python numpy
"""
import cv2

cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)          # cv2.CAP_DSHOW fixes MSMF capture errors on Windows
if not cap.isOpened():
    cap = cv2.VideoCapture(0)
if not cap.isOpened():
    print("Webcam not found. Check the cable or try VideoCapture(1).")
    raise SystemExit

info_text = "Click anywhere on the video to inspect a color"
color_name = ""
clicked_bgr = None
click_pos = None
state = {"frame": None}


def get_color_name(h, s, v):
    if v < 40:
        return "Black / Very Dark"
    if s < 30:
        return "White" if v > 200 else "Gray"
    if 35 <= h <= 85:
        return "Green (Green Screen Range)"
    elif 85 < h <= 135:
        return "Blue"
    elif 135 < h <= 165:
        return "Purple / Magenta"
    elif h > 165 or h <= 10:
        return "Red"
    elif 10 < h <= 25:
        return "Orange / Skin Tone"
    elif 25 < h < 35:
        return "Yellow"
    return "Custom"


def on_click(event, x, y, flags, param):
    global info_text, color_name, clicked_bgr, click_pos
    if event == cv2.EVENT_LBUTTONDOWN and state["frame"] is not None:
        frame = state["frame"]
        b, g, r = [int(v) for v in frame[y, x]]
        hsv = cv2.cvtColor(frame[y:y + 1, x:x + 1], cv2.COLOR_BGR2HSV)[0, 0]
        h, s, v = int(hsv[0]), int(hsv[1]), int(hsv[2])
        color_name = get_color_name(h, s, v)
        clicked_bgr = (b, g, r)
        click_pos = (x, y)
        info_text = f"BGR=({b},{g},{r})  HSV=({h},{s},{v})"
        print(f"[{color_name}] {info_text}")


cv2.namedWindow("Class 6 - Live Camera")
cv2.setMouseCallback("Class 6 - Live Camera", on_click)

while True:
    ok, frame = cap.read()
    if not ok:
        break
    state["frame"] = frame.copy()

    # Draw dark top banner for clear readable information
    cv2.rectangle(frame, (0, 0), (frame.shape[1], 75), (30, 30, 30), -1)

    if clicked_bgr is not None:
        # 1. Color Swatch Box showing the exact clicked color
        cv2.rectangle(frame, (12, 12), (65, 65), clicked_bgr, -1)
        cv2.rectangle(frame, (12, 12), (65, 65), (255, 255, 255), 2)

        # 2. Color Name & Value text
        cv2.putText(frame, f"Color: {color_name}", (78, 33),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.65, (0, 255, 255), 2)
        cv2.putText(frame, info_text, (78, 60),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.52, (220, 220, 220), 1)

        # 3. Crosshair marker at the clicked location
        cx, cy = click_pos
        cv2.circle(frame, (cx, cy), 9, (255, 255, 255), 2)
        cv2.circle(frame, (cx, cy), 6, clicked_bgr, -1)
        cv2.line(frame, (cx - 15, cy), (cx + 15, cy), (255, 255, 255), 1)
        cv2.line(frame, (cx, cy - 15), (cx, cy + 15), (255, 255, 255), 1)
    else:
        cv2.putText(frame, info_text, (15, 45),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 255), 2)
    cv2.imshow("Class 6 - Live Camera", frame)

    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

cap.release()
cv2.destroyAllWindows()
