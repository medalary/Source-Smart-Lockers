import cv2
import tkinter as tk
from PIL import Image, ImageTk
import numpy as np

CAMERA_WIDTH = 1200
CAMERA_HEIGHT = 2048
CAMERA_INDEX = 0
FULLSCREEN_MODE = True
WINDOW_TITLE = "Smart Locker Camera Interface"

TARGET_DISPLAY_WIDTH = 600
TARGET_DISPLAY_HEIGHT = 1024

BORDER_COLOR = (0, 255, 0)
BORDER_THICKNESS = 10
BORDER_WIDTH_RATIO = 0.7
BORDER_HEIGHT_RATIO = 0.6
BORDER_RADIUS = 30
SHORT_LINE_LENGTH = 50

def draw_rounded_corners_with_lines(image, p1, p2, color, thickness, r, line_length):
    x1, y1 = p1
    x2, y2 = p2

    cv2.ellipse(image, (x1 + r, y1 + r), (r, r), 180, 0, 90, color, thickness)
    cv2.ellipse(image, (x2 - r, y1 + r), (r, r), 270, 0, 90, color, thickness)
    cv2.ellipse(image, (x1 + r, y2 - r), (r, r), 90, 0, 90, color, thickness)
    cv2.ellipse(image, (x2 - r, y2 - r), (r, r), 0, 0, 90, color, thickness)

    cv2.line(image, (x1 + r, y1), (x1 + r + line_length, y1), color, thickness)
    cv2.line(image, (x2 - r, y1), (x2 - r - line_length, y1), color, thickness)

    cv2.line(image, (x1 + r, y2), (x1 + r + line_length, y2), color, thickness)
    cv2.line(image, (x2 - r, y2), (x2 - r - line_length, y2), color, thickness)

    cv2.line(image, (x1, y1 + r), (x1, y1 + r + line_length), color, thickness)
    cv2.line(image, (x1, y2 - r), (x1, y2 - r - line_length), color, thickness)

    cv2.line(image, (x2, y1 + r), (x2, y1 + r + line_length), color, thickness)
    cv2.line(image, (x2, y2 - r), (x2, y2 - r - line_length), color, thickness)

cap = cv2.VideoCapture(CAMERA_INDEX)
if not cap.isOpened():
    print(f"Error: Could not open camera with index {CAMERA_INDEX}. Please check connection or camera index.")
    exit()

cap.set(cv2.CAP_PROP_FRAME_WIDTH, CAMERA_WIDTH)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, CAMERA_HEIGHT)

actual_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
actual_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
print(f"Actual camera resolution set: {actual_width}x{actual_height}")
if actual_width != CAMERA_WIDTH or actual_height != CAMERA_HEIGHT:
    print(f"Warning: Camera does not exactly support {CAMERA_WIDTH}x{CAMERA_HEIGHT}. Using nearest supported resolution.")
    CAMERA_WIDTH = actual_width
    CAMERA_HEIGHT = actual_height

window = tk.Tk()
window.title(WINDOW_TITLE)

if FULLSCREEN_MODE:
    window.attributes('-fullscreen', True)
    window.bind('<Escape>', lambda e: window.attributes('-fullscreen', False))
    print("Press Esc to exit full-screen mode.")
    
    SCREEN_WIDTH = window.winfo_screenwidth()
    SCREEN_HEIGHT = window.winfo_screenheight()
    
    TARGET_DISPLAY_WIDTH = SCREEN_WIDTH
    TARGET_DISPLAY_HEIGHT = SCREEN_HEIGHT
else:
    window.geometry(f"{TARGET_DISPLAY_WIDTH}x{TARGET_DISPLAY_HEIGHT}")

label_widget = tk.Label(window, bg="black")
label_widget.pack(fill=tk.BOTH, expand=True)
def update_frame():
    ret, frame = cap.read()
    if ret:
        frame = cv2.flip(frame, 1)

        original_h, original_w, _ = frame.shape

        target_aspect_ratio = TARGET_DISPLAY_WIDTH / TARGET_DISPLAY_HEIGHT
        original_aspect_ratio = original_w / original_h

        crop_x, crop_y, crop_w, crop_h = 0, 0, original_w, original_h

        if original_aspect_ratio > target_aspect_ratio:
            crop_w = int(original_h * target_aspect_ratio)
            crop_x = (original_w - crop_w) // 2
        else:
            crop_h = int(original_w / target_aspect_ratio)
            crop_y = (original_h - crop_h) // 2
        
        cropped_frame = frame[crop_y : crop_y + crop_h, crop_x : crop_x + crop_w]

        border_w = int(cropped_frame.shape[1] * BORDER_WIDTH_RATIO)
        border_h = int(cropped_frame.shape[0] * BORDER_HEIGHT_RATIO)

        border_x1 = (cropped_frame.shape[1] - border_w) // 2
        border_y1 = (cropped_frame.shape[0] - border_h) // 2
        border_x2 = border_x1 + border_w
        border_y2 = border_y1 + border_h

        draw_rounded_corners_with_lines(cropped_frame, (border_x1, border_y1), (border_x2, border_y2),
                                        BORDER_COLOR, BORDER_THICKNESS, BORDER_RADIUS, SHORT_LINE_LENGTH)

        cv2_image = cv2.cvtColor(cropped_frame, cv2.COLOR_BGR2RGB)

        pil_image = Image.fromarray(cv2_image)

        label_width = label_widget.winfo_width()
        label_height = label_widget.winfo_height()

        if label_width == 1 and label_height == 1:
            label_width = TARGET_DISPLAY_WIDTH
            label_height = TARGET_DISPLAY_HEIGHT

        pil_image = pil_image.resize((label_width, label_height), Image.LANCZOS)

        tk_image = ImageTk.PhotoImage(pil_image)

        label_widget.imgtk = tk_image
        label_widget.config(image=tk_image)

    label_widget.after(10, update_frame)

update_frame()
def on_closing():
    print("Closing application and releasing camera.")
    cap.release()
    window.destroy()

window.protocol("WM_DELETE_WINDOW", on_closing)

window.mainloop()