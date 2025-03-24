# Gesture Mouse Control

## Overview
This project allows users to control their computer mouse using hand gestures via a webcam. It leverages MediaPipe for hand tracking and PyAutoGUI for simulating mouse actions. The project supports various gestures for movement, clicking, scrolling, and window management.

## Features
- **Cursor Control**: Move the cursor by tracking the index and middle fingers side by side.
- **Clicking**: Perform a left-click by pinching the index finger with the thumb.
- **Right-Click Menu**: Open the right-click menu by touching the ring finger with the thumb.
- **Scrolling**: Scroll up and down by pinching both the index and middle fingers with the thumb and moving vertically.
- **Drag & Drop**: Hold a pinch for a certain duration before moving to simulate drag and drop.
- **Minimize All Windows**: Clench your hand into a fist to minimize all open windows.
- **Restore Windows**: Unclench your hand to restore all minimized windows.

## Requirements
- Python 3.10
- OpenCV
- MediaPipe
- PyAutoGUI
- NumPy

## Installation
1. Clone the repository:
   ```sh
   git clone https://github.com/mostafa-31/gesture_mouse.git
   cd gesture_mouse
   ```
2. Create a virtual environment (optional but recommended):
   ```sh
   python -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`
   ```
3. Install dependencies:
   ```sh
   pip install -r requirements.txt
   ```

## Usage
Run the main script to start gesture recognition:
```sh
python main.py
```
Ensure your webcam is enabled and use the gestures described in the Features section.

## Troubleshooting
- **DLL Load Error (MediaPipe Issue)**: Try reinstalling MediaPipe with a compatible Python version:
  ```sh
  pip uninstall mediapipe
  pip install mediapipe
  ```
- **Cursor Movement Not Accurate**: Adjust sensitivity values in the script.
- **Gestures Not Recognized Properly**: Ensure proper lighting and clear hand visibility.

## Future Improvements
- Customizable gestures.
- Multi-hand support.
- Enhanced accuracy using AI models.

## License
MIT License
