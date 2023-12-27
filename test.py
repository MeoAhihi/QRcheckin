import cv2
import tkinter as tk
from tkinter import messagebox
from pyzbar.pyzbar import decode
import pandas as pd

class RegisteredList:
    def __init__(self, excel_file):
        self.registered = self.read_excel(excel_file)
        self.checkedIn = []

    def read_excel(self, excel_file):
        df = pd.read_excel(excel_file)
        return df["ID"].tolist()

    def getData(self):
        return self.registered

    def getCheckedIn(self):
        return self.checkedIn

    def isRegistered(self, ID):
        return ID in self.registered
    
    def getNameFromID(self, ID):
        for record in self.registered:
            if record == ID:
                return record==ID==['HọvàTên']
        return None
    
    def splitNamePhone(self, ID):
        phone = ID[:10]
        email = ID[10:]
        return phone, email

    def checkIn(self, ID):
        if self.isRegistered(ID):
            if ID in self.checkedIn:
                messagebox.showinfo("Duplicate ID", "ID {} has already been checked in.".format(ID))
            else:
                name = self.getNameFromID(ID)
                phone, email = self.splitNamePhone(ID)
                confirmation = messagebox.askquestion("Check-in Confirmation", "Bạn có phải là:\nHọ và Tên: {}\nSố điện thoại: {}\nEmail: {}?".format(name,phone, email))
                if confirmation == 'yes':
                    self.checkedIn.append(ID)
                    messagebox.showinfo("Check-in", "Chúc Mừng Bạn Đã Check-in Thành Công.")
                else:
                    messagebox.showinfo("Check-in", "Vui Lòng Cho Xin Lại Thông Tin Người Dùng.")
        else:
            messagebox.showinfo("Invalid ID", "ID {} is not registered.".format(ID))


class QRCodeScannerApp:
    def __init__(self, window, window_title, excel_file):
        self.registeredList = RegisteredList(excel_file)
        self.registered = self.registeredList.getData()

        self.window = window
        self.window.title(window_title)

        self.scan_here = tk.Label(
            text="Scan your ticket here", font=("Times New Roman", 50))
        self.scan_here.pack()

        self.video_source = 0  # 0 for the default camera
        self.vid = cv2.VideoCapture(self.video_source)

        self.canvas = tk.Canvas(
            window, width=self.vid.get(3), height=self.vid.get(4))
        self.canvas.pack()

        self.after_id = None
        self.confirmation_flag = False  # Cờ để kiểm tra xác nhận
        self.window.protocol("WM_DELETE_WINDOW", self.on_close)
        self.window.after(10, self.update)
        self.window.mainloop()

    def update(self):
        # scan the frame
        ret, frame = self.vid.read()
        if ret:
            self.showIMG(frame)
            data = self.scan_qr_code(frame)
            if data and not self.confirmation_flag:
                self.confirmation_flag = True  # Đánh dấu đã quét mã và chưa xác nhận
                self.registeredList.checkIn(data)
                self.confirmation_flag = False  # Đặt lại cờ sau khi xác nhận

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
app = QRCodeScannerApp(root, "QR Code Scanner App", "E:\C#\DANH SÁCH NGƯỜI THAM GIA PROM NIGHT 2023.xlsx")