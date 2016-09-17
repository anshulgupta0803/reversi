#!/usr/bin/python3

import socket
import sys
import signal
import threading
from functools import partial
from board import Board

WHITE = 0
BLACK = 1
EMPTY = 2
# PIECE[WHITE] = "X"
# PIECE[BLACK] = "O"
# PIECE[EMPTY] = "."
PIECE=["X", "O", "."]

class Serve(threading.Thread):
    def __init__(self, connection, address):
        threading.Thread.__init__(self)
        self.connection = connection
        self.address = address

    def run(self):
        print("[INFO] Got connection form", self.address)

        # Send acknowledgement for connecting
        msg="Welcome to Reversi\n\nChoose a color:\n0. White\n1. Black"
        self.connection.send(msg.encode("ascii"))

        # Wait for handshake packet
        handshakePacket = self.connection.recv(1024)
        packet=list(handshakePacket.decode("ascii").split(" "))
        if packet[0] == "initiate":
            print("[INFO] Opponent wants to play with", packet[1])

        if packet[1] == "white":
            myColor = BLACK
        elif packet[1] == "black":
            myColor = WHITE

        board = Board(myColor)
        board.printBoard()
        self.connection.close()

class Server():
    def __init__(self, port):
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.host = socket.gethostname()
        self.port = int(sys.argv[1])

    def run(self):
        try:
            self.s.bind((self.host, self.port))
        except Exception as e:
            print("[ERROR] Cannot bind the address")
            exit()

        # Will listen to 1 simultaneous connection
        self.s.listen(1)

        print("[INFO] Server running at port", self.port)
        while True:
            self.connection, self.address = self.s.accept()
            self.serve = Serve(self.connection, self.address);
            # Start a serving thread
            self.serve.start()

def terminate(server, signum, frame):
    print("\n[INFO] Shutting down the server...")
    server.s.close()
    exit()

def main():
    server = Server(sys.argv[1])
    # Terminates the server gracefully
    interruptHandler = signal.signal(signal.SIGINT, partial(terminate, server))
    server.run()

if __name__ == '__main__':
    main()
