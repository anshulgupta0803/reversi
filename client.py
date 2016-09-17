#!/usr/bin/python3

import socket
import sys

s = socket.socket()
host = socket.gethostname()
port = int(sys.argv[1])

try:
    s.connect((host, port))
except Exception as e:
    print("[ERROR] Unable to connect to server")
    exit()


msg = s.recv(1024)
s.close()
print("[INFO]", msg.decode('ascii'))
