import argparse
import asyncio
import sys
import time
from websockets.server import serve
import pickle
import socket
from motordriver import MotorDriver
from camera import Camera
from threading import *
import cv2

class Server:
    def __init__(self):
        self.camera = Camera()
        self.motors = MotorDriver()

    def get_sensors_data(self) -> dict:
        info = {
            "gyro": {"x": 0, "y": 0, "z": 0},
            "temperature": 99999
        }
        return info

    def handle_motors(self, info: dict):
        """
        {
            'forward': keyboard.is_pressed("w"),
            'backwards': keyboard.is_pressed("a"),
            'right': keyboard.is_pressed("s"),
            'left': keyboard.is_pressed("d"),
        }
        :param info:
        :return:
        """
        forward = info['forward']
        backwards = info['backwards']
        left = info['left']
        right = info['right']
        if forward:
            self.motors.move(1, 1)
        elif backwards:
            self.motors.move(-1, -1)
        elif right:
            self.motors.move(1, -1)
        elif left:
            self.motors.move(-1, 1)

        if info['cam_up']:
            self.motors.move_cam(1)
        elif info['cam_down']:
            self.motors.move_cam(-1)

        if info['led']:
            self.motors.set_led(50)
        else:
            self.motors.set_led(0)

        if info["stop"]:
            self.motors.hault_state(True)

    async def handle(self, websocket):
        async for message in websocket:
            data = pickle.loads(message)
            self.handle_motors(data["motor_control"])
            img = self.camera.get_image()
            compression = data['img_comp'] if 'img_comp' in data and abs(data['img_comp']) < 99 else 50
            encode_param = [int(cv2.IMWRITE_JPEG_QUALITY), compression]
            result, encimg = cv2.imencode('.jpeg', img, encode_param)
            response = {"cam": encimg, "sensors": self.get_sensors_data()}
            response = pickle.dumps(response)
            await websocket.send(response)

    async def run(self, IP:str="localhost", PORT: int=8000):
        if IP == None:
            host = socket.gethostname()
            IP = socket.gethostbyname(host)
            PORT = 8000 if PORT == None else PORT

        async with serve(self.handle, IP, PORT):
            HOST = f"ws://{IP}:{PORT}/"
            print(f"Server stated at address: {HOST}")
            await asyncio.Future()  # run forever

    def begin(self, IP:str="localhost", PORT: int=8000):
        server_thread = Thread(target=self.motors.drive_motor, args=(True,))
        server_thread.start()
        asyncio.run(self.run(IP, PORT))


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
    PORT = 8000 if PORT == None else PORT
    server = Server()
    server.begin(IP, PORT)
    sys.exit(0)



