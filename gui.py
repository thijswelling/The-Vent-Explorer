import datetime
import socket
import time
import tkinter as tk
from tkinter import ttk
from PIL import ImageTk, Image
from client import Client
import cv2
import argparse


class Gui(tk.Tk):
    def __init__(self, size=(1280, 720), host: str = "ws://192.168.1.12:8000/"):
        #   main setup
        super().__init__()
        self.wm_title("The vent Explorer")
        self.geometry(f'{size[0]}x{size[1]}')
        self.minsize(size[0], size[1])
        self.setup_camera_widget()
        self.setup_activity_log()
        self.client = Client(host=host)
        self.after(1, self.update_loop)
        self.image_quality = 5
        self.fps_latency = 0.1
        self.mainloop()

    def update_loop(self):
        keypress = self.client.read_keyboard_states()
        timer = time.time()
        states = self.client.pass_get_states(state=keypress, img_compression=self.image_quality)
        latency = round(time.time() - timer, 3)

        min_quality, max_quality = 5, 95
        self.image_quality += 1 if self.fps_latency > latency else -1
        self.image_quality = min_quality if self.image_quality < min_quality else self.image_quality
        self.image_quality = max_quality if self.image_quality > max_quality else self.image_quality

        if states["status"] == True:
            rgb_frame = cv2.cvtColor(states["cam"], cv2.COLOR_BGR2RGB)
            self.update_camera_frame(rgb_frame)
            txt = f"{states['sensors']} {keypress}  latency: {latency}"
        else:
            txt = states["error"]
        txt += f" img_quality: {self.image_quality}"
        self.add_text(txt)
        self.after(1, self.update_loop)

    def add_text(self, text: str):
        now = datetime.datetime.now()
        time_str = now.strftime("%H:%M:%S")
        self.text_display.insert(tk.END, f"{time_str}: {text}\n")
        self.text_display.see("end")

    def clear_text(self):
        self.text_display.setvar("state", "disabled")
        self.text_display.delete(1.0, tk.END)

    def setup_activity_log(self, relx=0, rely=1, relheight=0.2, relwidth=1):
        root = ttk.Frame(self)
        root.place(relx=relx, rely=rely, relwidth=relwidth, relheight=relheight, anchor='sw')
        self.text_display = tk.Text(root, fg='white', wrap=tk.WORD, background='black', font=('Verdana', 8), )
        self.text_scrollbar = tk.Scrollbar(root, command=self.text_display.yview)
        self.clear_button = ttk.Button(root, text="Clear", command=self.clear_text)

        # position objects
        self.text_scrollbar.place(rely=1, relx=1, width=25, relheight=1, anchor='se')
        self.clear_button.place(relx=1, rely=0, width=50, height=25, anchor="ne")
        self.text_display.config(yscrollcommand=self.text_scrollbar.set)
        self.text_display.place(relwidth=1, relx=0, rely=0, relheight=1, anchor='nw')

    def update_camera_frame(self, rgb_frame):
        photo = ImageTk.PhotoImage(image=Image.fromarray(rgb_frame))
        self.camera_canvas.create_image(0, 0, anchor=tk.NW, image=photo)
        self.camera_canvas.photo = photo

    def update_map_frame(self, frame: any=None):
        pass

    def setup_camera_widget(self):
        self.camera_canvas = tk.Canvas(self, width=1280, height=720)
        self.camera_canvas.place(relx=1, rely=1, relwidth=1, relheight=0.8)
        self.camera_canvas.pack()


parser = argparse.ArgumentParser(
    prog='Client',
    description='remote controller over websocket',
    epilog='yoooooo')
parser.add_argument('-ip')
parser.add_argument('-port')

if __name__ == '__main__':
    # parse args
    args = parser.parse_args()
    IP = args.ip
    PORT = args.port
    if IP is None:
        host = socket.gethostname()
        IP = socket.gethostbyname(host)

    # set params
    PORT = 8000 if PORT is None else PORT
    HOST = f"ws://{IP}:{PORT}/"

    gui = Gui(host=HOST)
