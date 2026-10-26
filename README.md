# Green Cloth - Real-Time Invisibility Cloak 🧙‍♂️🪄

A real-time computer vision project using Python and OpenCV that creates an "invisibility cloak" effect using a green cloth and background replacement.

## 🚀 Features

- **Color Science & Setup**: Explore RGB vs HSV color spaces.
- **Green Color Detection**: HSV mask thresholding with real-time tuning trackbars.
- **Background Replacement**: Morphological operations (erosion/dilation) to clean noise and blend background with the live video stream.
- **Integrated Live App**:
  - `b`: Capture and average initial background frames.
  - `m`: Toggle green mask window.
  - `c`: Compare original frame vs invisible cloak result side-by-side.
  - `s`: Save a screenshot.
  - `q`: Quit.

## 📁 Project Structure

```
├── class6_setup_and_color_science.py   # Webcam initialization and color space exploration
├── class7_green_detection.py           # Green detection using HSV thresholding
├── class8_background_replacement.py    # Segmenting and substituting background
├── class9_final_integrated_project.py  # Complete interactive invisibility cloak app
├── .gitignore
└── README.md
```

## 🛠️ Prerequisites & Installation

1. Install Python 3.8+
2. Install required packages:
```bash
pip install opencv-python numpy
```

## 🎮 How to Run

1. Run the final integrated project:
```bash
python class9_final_integrated_project.py
```
2. Stay out of the webcam frame and press **`b`** to capture the background.
3. Bring your green cloth in front of the camera and tune the HSV sliders as needed!
