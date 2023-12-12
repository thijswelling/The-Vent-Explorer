import asyncio, socket, pickle
import time

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.connect(('localhost', 15555))
request = None

try:
    while request != 'quit':
        request = "add"
        timer = time.time()
        if request:
            server.send(request.encode('utf8'))
            response = server.recv(921765)
            print(f"resp len: {len(response)} bytes time: {time.time()-timer}")

except KeyboardInterrupt:
    server.close()