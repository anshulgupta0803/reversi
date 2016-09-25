#!/usr/bin/python3

import socket
import sys
import signal
import threading
from functools import partial
from board import Board
import random

WHITE = 0
BLACK = 1
EMPTY = 2
# PIECE[WHITE] = "X"
# PIECE[BLACK] = "O"
# PIECE[EMPTY] = "."
PIECE = ["X", "O", "."]

EXIT = 100
INVALID = -10
PASS = -20

class Serve(threading.Thread):
	def __init__(self, connection, address):
		threading.Thread.__init__(self)
		self.connection = connection
		self.address = address
		self.board = ""

	def run(self):
		print("[INFO] Got connection form", self.address)

		# Send acknowledgement for connecting
		msg="Welcome to Reversi\n\n"
		self.connection.send(msg.encode("ascii"))

		# Wait for handshake packet
		handshakePacket = self.connection.recv(1024).decode("ascii")
		print("[INFO] Opponent ID is", handshakePacket)

		color = [WHITE, BLACK]
		myColor = color[random.randint(0, 1)]
		if myColor == WHITE:
			self.connection.send("START BLACK".encode("ascii"))
		else:
			self.connection.send("START WHITE".encode("ascii"))

		self.board = Board(myColor)
		gameInitialized = True
		self.board.printBoard()
		validMoves = self.board.legalMoves()
		print(validMoves)
		opponentPassed = False
		while not(self.board.isBoardFull() or (opponentPassed and len(validMoves) == 0)):
			# Black makes the first move
			if gameInitialized and self.board.myColor != BLACK:
				print("[DEBUG] Valid Moves:", validMoves)
				ij = validMoves[random.randint(0, len(validMoves) - 1)]
				self.board.updateBoard(ij, self.board.myColor)
				self.connection.send(ij.encode("ascii"))
				print("[DEBUG] You chose i:", ij[:1], "j:", ij[2:])
				self.board.printBoard()
				gameInitialized = False

			ij = self.connection.recv(1024).decode("ascii")
			if ij == "close":
				print("[INFO] Opponent left")
				self.board.printBoard()
				self.board.getFinalScore()
				break
			else:
				if ij == str(PASS):
					opponentPassed = True
					print("[INFO] Opponent passed")
				else:
					self.board.updateBoard(ij, self.board.opponentColor)
					print("[DEBUG] Opponent chose i:", ij[:1], "j:", ij[2:])
					self.board.printBoard()
				validMoves = self.board.legalMoves()
				if self.board.isBoardFull() or (opponentPassed and len(validMoves) == 0):
					print("[INFO] No valid moves remaining. Passing the turn")
					self.connection.send(str(PASS).encode("ascii"))
					break
				if len(validMoves) == 0:
					print("[INFO] No valid moves remaining. Passing the turn")
					self.connection.send(str(PASS).encode("ascii"))
				if len(validMoves) > 0:
					if opponentPassed:
						opponentPassed = False
					print("[DEBUG] Valid Moves:", validMoves)
					ij = validMoves[random.randint(0, len(validMoves) - 1)]
					self.board.updateBoard(ij, self.board.myColor)
					self.connection.send(ij.encode("ascii"))
					print("[DEBUG] You chose i:", ij[:1], "j:", ij[2:])
					self.board.printBoard()

		print("\n[INFO] Fetching final score...")
		self.board.getFinalScore()
		self.connection.close()

class Server():
	def __init__(self, port):
		self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		self.s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
		self.host = socket.gethostname()
		self.port = port

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
	try:
		port = int(sys.argv[1])
	except Exception as e:
		print("[ERROR] Usage:", sys.argv[0], "port")
		exit()
	server = Server(port)
	# Terminates the server gracefully
	interruptHandler = signal.signal(signal.SIGINT, partial(terminate, server))
	server.run()

if __name__ == '__main__':
	main()
