import asyncio, socket, pickle
import zlib
from camera import Camera
import cv2

camara = Camera()

img = camara.get_image()
encode_param = [int(cv2.IMWRITE_JPEG_QUALITY), 10]
result, encimg = cv2.imencode('.jpg', img, encode_param)

x = 0;
async def handle_client(client):
    loop = asyncio.get_event_loop()
    request = None
    while request != 'quit':
        request = (await loop.sock_recv(client, 255)).decode('utf8')
        print(request)
        img = camara.get_image()
        img_bin = pickle.dumps(img)
        print(f"send {len(img_bin)} bytes")
        await loop.sock_sendall(client, img_bin)
    client.close()

async def run_server():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(('localhost', 15555))
    server.listen(8)
    server.setblocking(False)

    loop = asyncio.get_event_loop()

    while True:
        client, _ = await loop.sock_accept(server)
        loop.create_task(handle_client(client))

if __name__ == '__main__':
    asyncio.run(run_server())