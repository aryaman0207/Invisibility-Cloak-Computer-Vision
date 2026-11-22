"""
Invisibility Cloak - Computer Vision Mini Project
-------------------------------------------------
Hides any cloth of a chosen colour by replacing it, frame by frame,
with a pre-captured picture of the empty background.

Controls (click the video window first):
    1 / 2 / 3 : cloak colour -> blue / red / green
    b         : re-capture the background (step out of the frame!)
    f         : toggle fullscreen
    m         : toggle mask view (useful for tuning colours)
    r         : start / stop recording to output.avi
    q         : quit
"""

import time
import cv2
import numpy as np

WINDOW = "Invisibility Cloak"
FONT = cv2.FONT_HERSHEY_SIMPLEX

# HSV ranges in OpenCV scale: H = 0-179, S = 0-255, V = 0-255.
# Red sits at both ends of the hue circle, so it needs two ranges.
CLOAK_COLORS = {
    "blue":  [((95, 90, 70), (130, 255, 255))],
    "red":   [((0, 120, 70), (10, 255, 255)),
              ((170, 120, 70), (179, 255, 255))],
    "green": [((40, 70, 70), (85, 255, 255))],
}
KEY_TO_COLOR = {ord("1"): "blue", ord("2"): "red", ord("3"): "green"}

KERNEL_SMALL = np.ones((3, 3), np.uint8)
KERNEL_LARGE = np.ones((7, 7), np.uint8)


def capture_background(cap, frames=60):
    """Grab several frames and take their per-pixel median.
    The median removes noise and any brief movement."""
    shots = []
    for i in range(frames):
        ok, frame = cap.read()
        if not ok:
            continue
        frame = cv2.flip(frame, 1)
        shots.append(frame)

        preview = frame.copy()
        cv2.putText(preview, f"Step out of the frame... {i + 1}/{frames}",
                    (20, 40), FONT, 0.8, (0, 255, 255), 2)
        cv2.imshow(WINDOW, preview)
        cv2.waitKey(30)

    if not shots:
        return None
    return np.median(np.stack(shots), axis=0).astype(np.uint8)


def make_cloak_mask(frame, color):
    """Return a clean binary mask (255 = cloak) for the chosen colour."""
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    mask = np.zeros(frame.shape[:2], np.uint8)
    for low, high in CLOAK_COLORS[color]:
        mask |= cv2.inRange(hsv, np.array(low), np.array(high))

    # Opening removes small specks; closing fills small holes in the cloak.
    mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, KERNEL_SMALL, iterations=2)
    mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, KERNEL_LARGE, iterations=2)
    mask = cv2.dilate(mask, KERNEL_SMALL, iterations=1)
    return mask


def blend(frame, background, mask):
    """Alpha-blend: background where the cloak is, live frame elsewhere.
    Blurring the mask edge gives a soft, natural-looking border."""
    alpha = cv2.GaussianBlur(mask, (15, 15), 0).astype(np.float32) / 255.0
    alpha = alpha[:, :, None]
    out = background * alpha + frame * (1.0 - alpha)
    return out.astype(np.uint8)


def main():
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        print("Could not open the camera.")
        return

    # Ask the camera for HD (it keeps its own maximum if HD is unsupported)
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)

    # WINDOW_NORMAL lets the window be resized / maximised
    cv2.namedWindow(WINDOW, cv2.WINDOW_NORMAL)
    cv2.resizeWindow(WINDOW, 1280, 720)
    fullscreen = False
    background = capture_background(cap)
    if background is None:
        print("Could not capture the background.")
        cap.release()
        return

    color = "blue"
    show_mask = False
    writer = None
    last_time = time.time()
    fps = 0.0

    while True:
        ok, frame = cap.read()
        if not ok:
            break
        frame = cv2.flip(frame, 1)

        mask = make_cloak_mask(frame, color)
        output = blend(frame, background, mask)

        if show_mask:
            display = cv2.cvtColor(mask, cv2.COLOR_GRAY2BGR)
        else:
            display = output.copy()

        now = time.time()
        fps = 0.9 * fps + 0.1 * (1.0 / max(now - last_time, 1e-6))
        last_time = now
        status = f"Cloak: {color} | FPS: {fps:.0f}"
        if writer is not None:
            status += " | REC"
        cv2.putText(display, status, (10, 25), FONT, 0.6, (0, 255, 0), 2)

        cv2.imshow(WINDOW, display)
        if writer is not None:
            writer.write(output)  # save without the text overlay

        key = cv2.waitKey(1) & 0xFF
        if key == ord("q"):
            break
        elif key in KEY_TO_COLOR:
            color = KEY_TO_COLOR[key]
        elif key == ord("f"):
            fullscreen = not fullscreen
            cv2.setWindowProperty(
                WINDOW, cv2.WND_PROP_FULLSCREEN,
                cv2.WINDOW_FULLSCREEN if fullscreen else cv2.WINDOW_NORMAL)
        elif key == ord("m"):
            show_mask = not show_mask
        elif key == ord("b"):
            background = capture_background(cap)
            if background is None:
                break
        elif key == ord("r"):
            if writer is None:
                h, w = output.shape[:2]
                writer = cv2.VideoWriter(
                    "output.avi", cv2.VideoWriter_fourcc(*"XVID"), 20, (w, h))
            else:
                writer.release()
                writer = None

    if writer is not None:
        writer.release()
    cap.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    main()