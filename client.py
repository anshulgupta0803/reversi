#!/usr/bin/python3

import socket
import sys
import signal
from functools import partial
import time
from board import Board
import os
import random
from ai import AI

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

HUMAN = 1
COMPUTER = 2

class Client():
	def __init__(self, host, port):
		self.s = socket.socket()
		self.host = host
		self.port = port
		self.board = ""
		self.gameActive = False

	def handshake(self, handshakePacket):
		self.s.send(handshakePacket.encode("ascii"))

	def run(self):
		try:
			self.s.connect((self.host, self.port))
		except Exception as e:
			print("[ERROR] Unable to connect to server")
			exit()

		# msg = self.s.recv(1024).decode("ascii")
		# print(msg)
		# Do a handshake
		handshakePacket = input("Roll Number: ")
		handshakePacket = handshakePacket + "\n"
		self.handshake(handshakePacket)

		# Wait for color message
		msg = self.s.recv(1024)
		print("[INFO]", msg.decode("ascii"))

		colorChosen = False
		while not(colorChosen):
			try:
				color = msg.decode("ascii").strip("\n").split(" ")[1]
				if color == "WHITE":
					myColor = WHITE
				elif color == "BLACK":
					myColor = BLACK
			except Exception as e:
				print("[WARN] Invalid color")
				continue

			if myColor == WHITE:
				print("\n[INFO] Your color is White (" + PIECE[WHITE] + ")")
				print("[INFO] Opponents's color is Black (" + PIECE[BLACK] + ")")
				colorChosen = True
			elif myColor == BLACK:
				print("\n[INFO] Your color is Black (" + PIECE[BLACK] + ")")
				print("[INFO] Opponents's color is White (" + PIECE[WHITE] + ")")
				colorChosen = True
			else:
				print("[WARN] Invalid color")

		playerTypeChosen = False
		while not(playerTypeChosen):
			print("1. Human v/s Computer")
			print("2. Computer v/s Computer")
			playerType = input("Enter choice: ")
			try:
				playerType = int(playerType)
			except Exception as e:
				print("[WARN] Invalid player type")
				continue

			if playerType == HUMAN:
				print("[INFO] Human v/s Computer")
				playerTypeChosen = True
			elif playerType == COMPUTER:
				print("[INFO] Computer v/s Computer")
				playerTypeChosen = True
			else:
				print("[WARN] Invalid player type")

		self.board = Board(myColor)
		gameInitialized = True
		self.gameActive = True
		self.board.printBoard()
		opponentPassed = False

		validMoves = self.board.legalMoves()
		while not(self.board.isBoardFull() or (opponentPassed and len(validMoves) == 0)):
			# Black makes the first move
			if gameInitialized and self.board.myColor == BLACK:
				ij = self.s.recv(1024).decode("ascii")
				self.board.updateBoard(ij, self.board.opponentColor)
				print("[DEBUG] Opponent chose i:", ij[:1], "j:", ij[2:])
				self.board.printBoard()
				validMoves = self.board.legalMoves()
				gameInitialized = False

			if (len(validMoves) == 0):
				move = str(PASS)
			else:
				if opponentPassed:
					opponentPassed = False
				print("[DEBUG] Valid Moves:", validMoves)
				if playerType == HUMAN:
					move = input("Your move (100 to exit): ")
				elif playerType == COMPUTER:
					move = validMoves[random.randint(0, len(validMoves) - 1)]
			ij = self.board.validateMove(move)
			if ij == EXIT:
				# Send SIGINT so that the trap handler can handle it
				os.kill(os.getpid(), signal.SIGINT)
			elif ij == INVALID:
				print("[WARN] Invalid move")
			else:
				if ij != PASS:
					self.board.updateBoard(ij, self.board.myColor)
					ij = ij + "\n"
					self.s.send(ij.encode("ascii"))
					print("[DEBUG] You chose i:", ij[:1], "j:", ij[2:])
					self.board.printBoard()
					if self.board.isBoardFull():
						break
				else:
					print("[INFO] No valid moves remaining. Passing the turn")
					ij = str(ij) + "\n"
					self.s.send(str(ij).encode("ascii"))
				ij = self.s.recv(1024).decode("ascii")
				if ij != str(PASS):
					self.board.updateBoard(ij, self.board.opponentColor)
					print("[DEBUG] Opponent chose i:", ij[:1], "j:", ij[2:])
					self.board.printBoard()
				else:
					opponentPassed = True
					print("[INFO] Opponent passed")
			validMoves = self.board.legalMoves()

		print("\n[INFO] Fetching final score...")
		self.board.getFinalScore()
		self.s.close()

def terminate(client, signum, frame):
	choice = input("\nDo you really want to quit (y/n)? ")
	if choice.lower().startswith("y"):
		if client.gameActive:
			client.s.send("close".encode("ascii"))
			print("\n[INFO] Fetching final score...")
			client.board.getFinalScore()
		print("\n[INFO] Quitting the game...")
		client.s.close()
		exit()
	else:
		print("\n[INFO] Continuing with the game...")
		pass

def main():
	try:
		host = sys.argv[1]
		port = int(sys.argv[2])
	except Exception as e:
		print("[ERROR] Usage:", sys.argv[0], "host port")
		exit()
	client = Client(host, port)
	# Terminates the client gracefully
	interruptHandler = signal.signal(signal.SIGINT, partial(terminate, client))
	client.run()

if __name__ == '__main__':
	main()
