import cv2
import tkinter as tk
from tkinter import messagebox
from pyzbar.pyzbar import decode


class RegisteredList:
    def __init__(self):
        self.registered = {
            "TEAM HOI DAP IS DA BEST!": 1,
            "https://myqr.pro/5f69885602f760": 2,
            "https://irrelevant-jellyfish.jurassic.ninja/2023/05/22/new/": 3,
            "http://www.maptitecreation.fr": 4,
            "https://luatbaoloi.com": 5,
            "https://skhdt.binhdinh.gov.vn/vi/thu-tuc-hanh-chinh/thu-tuc-dang-ky-doanh-nghiep.html": 6,
            "https://www.1check.vn/": 7,
            "http://bvu.edu.vn": 8,
        }
        self.checkedIn = []

    def getData(self):
        return self.registered

    def getCheckedIn(self):
        return self.checkedIn

    def isRegistered(self, ID):
        return ID in self.registered

    def checkIn(self, ID):
        if self.isRegistered(ID):
            self.checkedIn.append(ID)
            pass


class QRCodeScannerApp:
    def __init__(self, window, window_title):
        self.registeredList = RegisteredList()
        self.registered = self.registeredList.getData()

        self.window = window
        self.window.title(window_title)

        self.scan_here = tk.Label(
            text="Scan your ticket here", font=("Tahoma", 20))
        self.scan_here.pack()

        self.video_source = 0  # 0 for the default camera
        self.vid = cv2.VideoCapture(self.video_source)

        self.canvas = tk.Canvas(
            window, width=self.vid.get(3), height=self.vid.get(4))
        self.canvas.pack()

        self.after_id = None
        self.window.protocol("WM_DELETE_WINDOW", self.on_close)
        self.window.after(10, self.update)
        self.window.mainloop()

    def update(self):
        # scan the frame
        ret, frame = self.vid.read()
        if ret:
            self.showIMG(frame)
            data = self.scan_qr_code(frame)
            self.registeredList.checkIn(data)
            print(self.registeredList.getCheckedIn())

        self.after_id = self.window.after(10, self.update)

    def scan_qr_code(self, frame):
        decoded_objects = decode(frame)
        if decoded_objects:
            return decoded_objects[0].data.decode('utf-8')

    def showIMG(self, frame):
        self.photo = cv2.cvtColor(frame, cv2.COLOR_BGR2BGRA)
        self.photo = tk.PhotoImage(data=cv2.imencode(
            '.png', self.photo)[1].tobytes())
        self.canvas.create_image(0, 0, image=self.photo, anchor=tk.NW)

    def on_close(self):
        if self.after_id:
            self.window.after_cancel(self.after_id)
        self.vid.release()
        self.window.destroy()


# Create a window and pass it to the QRCodeScannerApp class
root = tk.Tk()
app = QRCodeScannerApp(root, "QR Code Scanner App")
