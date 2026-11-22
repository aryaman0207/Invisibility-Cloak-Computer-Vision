# Invisibility Cloak – Computer Vision Mini Project

## Overview
This project creates an invisibility-cloak effect using Python, OpenCV, and NumPy. It detects a selected colour of cloth (blue, red, or green) in a live webcam feed and replaces the detected area with a previously captured background.

## Features
- Real-time webcam processing
- Blue, red, and green cloak colour selection
- Background capture using multiple frames
- HSV colour-based segmentation
- Noise reduction using morphological operations
- Soft mask blending for smoother edges
- FPS display
- Fullscreen mode
- Mask visualization mode
- Video recording to `output.avi`

## Technologies Used
- Python
- OpenCV
- NumPy

## Requirements
- Python 3
- A working webcam
- Blue, red, or green cloth
- A reasonably steady background and consistent lighting

## Installation

1. Clone this repository:

   ```bash
   git clone YOUR_REPOSITORY_URL
   ```

2. Open the project folder:

   ```bash
   cd YOUR_REPOSITORY_FOLDER
   ```

3. Install the required packages:

   ```bash
   pip install -r requirements.txt
   ```

## Run the Project

```bash
python invisibility_cloak.py
```

When the program starts, step out of the camera view while it captures the background. After the capture is complete, stand in front of the camera wearing the selected colour cloth.

## Keyboard Controls

| Key | Action |
| --- | --- |
| `1` | Select blue cloak |
| `2` | Select red cloak |
| `3` | Select green cloak |
| `B` | Capture the background again (step out of the frame) |
| `F` | Toggle fullscreen |
| `M` | Toggle mask view |
| `R` | Start or stop recording to `output.avi` |
| `Q` | Quit the application |

Click the video window before using the keyboard controls.

## How It Works

1. The program captures multiple webcam frames while the background is empty.
2. It combines those frames using a per-pixel median to create a background image.
3. Each live frame is converted from BGR to HSV colour space.
4. A colour mask is created for the selected cloak colour.
5. Morphological operations reduce small noise and fill small gaps in the mask.
6. The mask is blurred and used to blend the captured background into the live frame wherever the selected colour is detected.
7. The resulting frame is displayed in real time.

## Notes
- Keep the camera and background as still as possible after capturing the background.
- Avoid wearing other objects with the selected cloak colour, as they may also be detected.
- Lighting and cloth shades affect colour detection. The HSV ranges in `invisibility_cloak.py` may need adjustment for different environments.
- The recording file `output.avi` is created in the current working directory when recording is enabled.

## Project Type
Computer Vision | Image Processing | Python
