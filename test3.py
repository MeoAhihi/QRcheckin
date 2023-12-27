import tkinter as tk
from PIL import Image, ImageTk
import pyfiglet

root = tk.Tk()

# Tạo đối tượng Figlet để tạo hình ảnh từ văn bản
figlet = pyfiglet.Figlet(font='big')

text = "Hello, World!"
ascii_art = figlet.renderText(text)

# Tạo hình ảnh từ văn bản ASCII sử dụng Pillow
image = Image.fromarray(ascii_art.encode())

# Chuyển đổi hình ảnh thành định dạng phù hợp với Tkinter
photo = ImageTk.PhotoImage(image)

# Tạo một nhãn và gắn hình ảnh vào đó
label = tk.Label(root, image=photo)
label.pack()

root.mainloop()