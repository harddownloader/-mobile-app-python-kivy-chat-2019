#!/usr/bin/env python3

import socket
import json

HOST = '127.0.0.1'  # The server's hostname or IP address
PORT = 8000        # The port used by the server

name = b'r'
temp_template = {'name': 'name'}

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect((HOST, PORT))
    # s.sendall(b'Hello, world')
    b = json.dumps(temp_template).encode('utf-8')
    s.sendall(b)
    data = s.recv(2048)
    # s.send(b'hi, man!')

print('Received', repr(data.decode()))