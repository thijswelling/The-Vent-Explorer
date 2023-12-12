import argparse
import json
import pickle
import time
import cv2
import numpy
from websockets.sync.client import connect
import keyboard
import socket
import numpy as np


class Client:
    def __init__(self, host: str = "ws://localhost:8000/"):
        self.host = host

    def pass_get_states(self) -> dict:
        with connect(self.host) as websocket:
            request = {"motor_control": self.read_keyboard_states()}
            print(request)
            request = pickle.dumps(request)
            websocket.send(request)
            message = websocket.recv()
            data = pickle.loads(message)
            response = {
                "status": True,
                "cam": data["cam"],
                "sensors": data["sensors"]
            }
            return response

    def read_keyboard_states(self) -> dict:
        keypressed = {
            'forward': keyboard.is_pressed("w"),
            'backwards': keyboard.is_pressed("s"),
            'right': keyboard.is_pressed("a"),
            'left': keyboard.is_pressed("d"),
        }
        return keypressed

    def show_image(self, frame: numpy.array):
        if type(frame) == numpy.ndarray:
            decoded_image = cv2.imdecode(np.frombuffer(frame, dtype=np.uint8), cv2.IMREAD_COLOR)

            cv2.imshow('frame', decoded_image)
            cv2.waitKey(1)
        return frame

    def run(self):
        print(f"running client with target host: {self.host}")
        while 1:
            timer = time.time()
            data = self.pass_get_states()
            print(time.time()-timer)
            self.show_image(frame=data["cam"])

            # print(data["sensors"])
            time.sleep(1 / 30)



parser = argparse.ArgumentParser(
    prog='Client',
    description='remote controller over websocket',
    epilog='yoooooo')
parser.add_argument('-ip')
parser.add_argument('-port')

if __name__ == '__main__':
    args = parser.parse_args()
    IP = args.ip
    PORT = args.port

    if IP == None:
        host = socket.gethostname()
        IP = socket.gethostbyname(host)
    print(PORT)
    PORT = 8000 if PORT == None else PORT
    HOST = f"ws://{IP}:{PORT}/"
    client = Client(HOST)
    client.run()
