import tkinter as tk
import cv2

# Constants for configeration
WINDOW_TITLE = "Glittering - Prompt Night Check-in"
DEFAULT_CAMERA = 0
FPS = 24

# Create window for display
window = tk.Tk()
window.title(WINDOW_TITLE)

# Open Camera
video = cv2.VideoCapture(DEFAULT_CAMERA)

# Create black canvas for video
canvas = tk.Canvas(window, width=video.get(3), height=video.get(4))
canvas.pack()

# Read a frame from the camera
_, frame = video.read()

# Put image into canvas
photo = cv2.cvtColor(frame, cv2.COLOR_BGR2BGRA)
photo = tk.PhotoImage(data=cv2.imencode('.png', photo)[1].tobytes())
canvas.create_image(0, 0, image=photo, anchor=tk.NW)

# window.after(int(1000/FPS), update)


def update():
    # global window, canvas
    # Read a frame from the camera
    _, frame = video.read()

    # Put image into canvas
    photo = cv2.cvtColor(frame, cv2.COLOR_BGR2BGRA)
    photo = tk.PhotoImage(data=cv2.imencode('.png', photo)[1].tobytes())
    canvas.create_image(0, 0, image=photo, anchor=tk.NW)

    window.after(int(1000/FPS), update)


def on_close():
    # Release all things afterward
    video.release()
    cv2.destroyAllWindows()
    window.destroy()


window.protocol("WM_DELETE_WINDOW", on_close)
window.after(int(1000/FPS), update)
window.mainloop()
