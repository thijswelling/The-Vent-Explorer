import argparse
import pickle
import time
import cv2
import numpy
from websockets.sync.client import connect
import keyboard
import socket


class Client:
    def __init__(self, host: str = "ws://localhost:8000/"):
        self.host = host
        self.lights_state = False
        self.light_toggle_prev = False

    def pass_get_states(self, state: dict or None = None, img_compression: int = 50) -> dict:
        response = {
            "status": False,
            "cam": None,
            "sensors": None,
            "error": None
        }
        try:
            with connect(self.host) as websocket:
                request = {"motor_control": self.read_keyboard_states() if state == None else state}
                request.update({'img_comp': img_compression})
                request = pickle.dumps(request)
                websocket.send(request)
                message = websocket.recv()
                data = pickle.loads(message)
                decoded_img = cv2.imdecode(data["cam"], 1)
                response['cam'] = decoded_img
                response["sensors"] = data["sensors"]
                response['status'] = True
        except Exception as e:
            response["error"] = f"unable to connect to host at {self.host}, except -> {e}"
        return response

    def read_keyboard_states(self) -> dict:
        pressed = keyboard.is_pressed("l")
        toggled = True if pressed != self.light_toggle_prev else False
        self.lights_state = (not self.lights_state) if toggled and self.light_toggle_prev else self.lights_state
        self.light_toggle_prev = pressed
        keypressed = {
            'forward': keyboard.is_pressed("up"),
            'backwards': keyboard.is_pressed("down"),
            'right': keyboard.is_pressed("right"),
            'left': keyboard.is_pressed("left"),
            'cam_up': keyboard.is_pressed("w"),
            'cam_down': keyboard.is_pressed("s"),
            'led': self.lights_state,
            'stop': keyboard.is_pressed("space")
        }
        return keypressed

    def show_image(self, frame: numpy.array):
        if type(frame) == numpy.ndarray:
            decoded_image = cv2.imdecode(frame, 1)
            cv2.imshow('frame', decoded_image)
            cv2.waitKey(1)
        return frame

    def run(self, fps: int = 30):
        print(f"running client with target host: {self.host}")
        while 1:
            data = self.pass_get_states()
            self.show_image(frame=data["cam"])
            print(data["sensors"])
            time.sleep(1 / fps)


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

    # run client
    client = Client(HOST)
    client.run()
