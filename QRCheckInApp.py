import cv2
import tkinter as tk
from tkinter import messagebox
from pyzbar.pyzbar import decode
import pandas as pd
from PIL import Image, ImageTk


class RegisteredList:
    def __init__(self, excel_file):
        self.registered = self.read_excel(excel_file)
        self.checkedIn = []

    def read_excel(self, excel_file):
        df = pd.read_excel(excel_file)
        return df.to_dict('records')

    def getData(self):
        return self.registered

    def getCheckedIn(self):
        return self.checkedIn

    def isRegistered(self, ID):
        return any(record['ID'] == ID for record in self.registered)

    def getNameFromID(self, ID):
        for record in self.registered:
            if record['ID'] == ID:
                return record['HọvàTên']
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
                phone, email = self.splitNamePhone(ID)
                name = self.getNameFromID(ID)
                if name is None:
                    messagebox.showinfo("Invalid ID", "Invalid ID: {}".format(ID))
                else:
                    confirmation = messagebox.askquestion("Check-in Confirmation", "Bạn có phải là:\nHọ và Tên:{}\nSố điện thoại:{}\nEmail:{}?".format(name,phone,email))
                    if confirmation == 'yes':
                        self.checkedIn.append(ID)
                        messagebox.showinfo("Check-in", "Chúc Mừng Bạn Đã Check-in Thành Công.")
                    else:
                        messagebox.showinfo("Check-in", "Vui Lòng Cho Xin Thông Tin Người Dùng.")
        else:
            if not self.isRegistered(ID):
                messagebox.showerror('Lỗi', 'Mã QR Không Hợp Lệ')


class QRCodeScannerApp:
    def __init__(self, window, window_title, excel_file):
        self.registeredList = RegisteredList(excel_file)
        self.registered = [record['ID'] for record in self.registeredList.getData()]

        self.window = window
        self.window.title(window_title)

        # Tạo đối tượng hình ảnh từ tệp PNG
        image = Image.open(image_path)

        # Lấy kích thước của cửa sổ
        window_width = self.window.winfo_screenwidth()
        window_height = self.window.winfo_screenheight()

        # Resize hình ảnh để phù hợp với kích thước cửa sổ
        resized_image = image.resize((window_width, window_height))
        self.background_image = ImageTk.PhotoImage(resized_image)
        self.background_label = tk.Label(window, image=self.background_image)
        self.background_label.place(x=0, y=0, relwidth=1, relheight=1)

        frame = tk.Frame(window)
        frame.place(relx=0.5, rely=0.5, anchor='center')
        self.scan_here = tk.Label(
            frame,text="QUÉT MÃ QR ĐÃ ĐƯỢC GỬI QUA EMAIL ĐỂ CHECK-IN", font=("Times New Roman", 19), fg="white")
        self.scan_here.configure(background="#%02x%02x%02x" % (0, 0, 0))
        self.scan_here.pack()

        self.video_source = 0  # 0 for the default camera
        self.vid = cv2.VideoCapture(self.video_source)

        self.canvas = tk.Canvas(
            master=frame, width=self.vid.get(3), height=self.vid.get(4))
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
        try:
            decoded_objects = decode(frame)
            if decoded_objects:
                return decoded_objects[0].data.decode('utf-8')
        except Exception as e:
            print("Error decoding QR code:", e)

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
image_path = "C:\\Users\\lehoa\\OneDrive\\Desktop\\Base prom poster [Recov-01.png"
app = QRCodeScannerApp(root, "QR Code Scanner App", "E:\\C#\\DANH SÁCH NGƯỜI THAM GIA PROM NIGHT 2023.xlsx")
root.mainloop()