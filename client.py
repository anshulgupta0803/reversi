#!/usr/bin/python3

import socket
import sys
import signal
from functools import partial
import time
from board import Board
from io import StringIO

WHITE = 0
BLACK = 1
EMPTY = 2
# PIECE[WHITE] = "X"
# PIECE[BLACK] = "O"
# PIECE[EMPTY] = "."
PIECE=["X", "O", "."]

class Client():
    def __init__(self, host, port):
        self.s = socket.socket()
        self.host = host
        self.port = port

    def handshake(self, color):
        handshakePacket = "initiate " + color
        self.s.send(handshakePacket.encode("ascii"))

    def run(self):
        try:
            self.s.connect((self.host, self.port))
        except Exception as e:
            print(e)
            print("[ERROR] Unable to connect to server")
            exit()

        # Wait for welcome message and color options
        msg = self.s.recv(1024)
        print("[INFO]", msg.decode("ascii"))

        colorChosen = False
        while not(colorChosen):
            myColor = input("Enter choice: ")
            if int(myColor) == WHITE:
                print("\n[INFO] Your color is White (" + PIECE[WHITE] + ")")
                print("[INFO] Opponents's color is black (" + PIECE[BLACK] + ")")
                colorChosen = True
                self.handshake("white")
            elif int(myColor) == BLACK:
                print("\n[INFO] Your color is black (" + PIECE[BLACK] + ")")
                print("[INFO] Opponents's color is white (" + PIECE[WHITE] + ")")
                colorChosen = True
                self.handshake("black")
            else:
                print("[WARN] Invalid color")


        board = Board(int(myColor))
        board.printBoard()
        self.s.close()

def terminate(client, signum, frame):
    choice = input("Do you really want to quit (y/n)? ")
    if choice.lower().startswith("y"):
        print("\n[INFO] Fetching final score...")
        # TODO Put code here to fetch final score
        # TODO Server should initialize the scoreboard in beginning
        print("\n[INFO] Quitting the game...")
        client.s.close()
        exit()
    else:
        print("\n[INFO] Continuing with the game...")
        pass

def main():
    client = Client(sys.argv[1], int(sys.argv[2]))
    # Terminates the client gracefully
    interruptHandler = signal.signal(signal.SIGINT, partial(terminate, client))
    client.run()

if __name__ == '__main__':
    main()
