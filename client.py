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
EXIT = 3
# PIECE[WHITE] = "⚪"
# PIECE[BLACK] = "⏺"
# PIECE[EMPTY] = "∙"
PIECE = [u"\u26AA", u"\u23FA", u"\u2219"]

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

	def connect(self):
		try:
			self.s.connect((self.host, self.port))
		except Exception as e:
			print("[ERROR] Unable to connect to server")
			exit()

		# Handle can be any string.
		print("[INFO] Sending handshake packet")
		handshakePacket = input("Enter your Handle: ")
		handshakePacket = handshakePacket + "\n"
		self.handshake(handshakePacket)

		# Wait for color message
		# Server sends a string: START WHITE or START BLACK
		print("[INFO] Waiting for color message")
		msg = self.s.recv(1024).decode("ascii")
		print("[INFO]", msg)
		# Return WHITE or BLACK depending on the string received from server
		return msg.strip("\n").split(" ")[1]

	def run(self, color):
		# Initialization stuff begins here
		try:
			if color == "WHITE":
				myColor = WHITE
			elif color == "BLACK":
				myColor = BLACK
			else:
				raise
		except Exception as e:
			print("[ERROR] Invalid color")
			exit()

		if myColor == WHITE:
			print("[INFO] Your color is White (" + PIECE[WHITE] + ")")
			print("[INFO] Opponents's color is Black (" + PIECE[BLACK] + ")")
			colorChosen = True
		elif myColor == BLACK:
			print("[INFO] Your color is Black (" + PIECE[BLACK] + ")")
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
				intelligence = input("Intelligence [1-4]: ")
				try:
					intelligence = int(intelligence)
					if intelligence < 1 or intelligence > 4:
						raise Exception
				except Exception as e:
					print("[WARN] Invalid value for intelligence")
					print("[WARN] Choosing lowest intelligence")
					intelligence = 1
				playerTypeChosen = True
			else:
				print("[WARN] Invalid player type")

		self.board = Board(myColor)
		gameInitialized = True
		self.gameActive = True
		self.board.printBoard()
		opponentPassed = False
		# Initialization stuff ends here

		validMoves = self.board.legalMoves()
		# Game ends when either board is full or both players are out of moves
		# Out of move condition is when opponent has passed and the current player has no moves left
		while not(self.board.isBoardFull() or (opponentPassed and len(validMoves) == 0)):
			# White makes the first move so wait for opponent if myColor is BLACK
			if gameInitialized and self.board.myColor == BLACK:
				print("[INFO] Waiting for opponent")
				ij = self.s.recv(1024).decode("ascii").strip("\n")
				if ij == "START WHITE" or ij == "START BLACK":
					print("[INFO]", ij)
					color = ij.split(" ")[1]
					return color

				self.board.updateBoard(ij, self.board.opponentColor)
				#print("[DEBUG] Opponent chose i:", ij[:1], "j:", ij[2:])
				self.board.printBoard()
				validMoves = self.board.legalMoves()

			if gameInitialized and playerType == COMPUTER:
				# Initialize AI
				brain = AI(self.board, intelligence)
				gameInitialized = False

			if len(validMoves) == 0:
				# If we are out of move, then pass
				move = str(PASS)
			else:
				if opponentPassed:
					opponentPassed = False

				if playerType == HUMAN:
					print("[DEBUG] Valid Moves:", validMoves)
					move = input("Your move (100 to exit): ")
				elif playerType == COMPUTER:
					print("[INFO] Thinking with Intelligence Level", intelligence)
					print("[INFO] Creating Tree")
					brain = AI(self.board, intelligence)
					print("[INFO] Minimax")
					brain.think()
					move = brain.getMove()

			# This ij will store the move that we will play
			ij = self.board.validateMove(move)

			if ij == EXIT:
				# Send SIGINT so that the trap handler can handle it
				os.kill(os.getpid(), signal.SIGINT)
			elif ij == INVALID:
				#print("[WARN] Invalid move")
				#print("Wrong Move:", move)
				continue
			else:
				if ij != PASS:
					# Update the board with the best move and send that move to the opponenet
					self.board.updateBoard(ij, self.board.myColor)
					ij = ij + "\n"
					self.s.send(ij.encode("ascii"))
					#print("[DEBUG] You chose i:", ij[:1], "j:", ij[2:])
					self.board.printBoard()
					if self.board.isBoardFull():
						break
				else:
					print("[INFO] No valid moves remaining. Passing the turn")
					ij = str(ij) + "\n"
					self.s.send(str(ij).encode("ascii"))

				print("[INFO] Waiting for opponent")
				# This ij will store the opponent's move
				ij = self.s.recv(1024).decode("ascii").strip("\n")

				# Ignore this
				if ij == "START WHITE" or ij == "START BLACK":
					print("[INFO]", ij)
					color = ij.split(" ")[1]
					return color

				if ij != str(PASS):
					self.board.updateBoard(ij, self.board.opponentColor)
					#print("[DEBUG] Opponent chose i:", ij[:1], "j:", ij[2:])
					#print("[INFO] Observing opponent's move")
					# brain.observe(ij)
					self.board.printBoard()
				else:
					opponentPassed = True
					print("[INFO] Opponent passed")
			validMoves = self.board.legalMoves()

		print("\n[INFO] Fetching final score...")
		self.board.getFinalScore()
		self.s.close()
		return EXIT

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
	# Get IP and PORT from user
	try:
		host = sys.argv[1]
		port = int(sys.argv[2])
	except Exception as e:
		# Exception when there is error in input from user
		print("[ERROR] Usage:", sys.argv[0], "IP", "PORT")
		exit()

	# Initialize client with host and port
	client = Client(host, port)

	# Terminates the client gracefully
	interruptHandler = signal.signal(signal.SIGINT, partial(terminate, client))

	# Connect to the server and server will assign a color to client
	color = client.connect()
	while True:
		color = client.run(color)
		if color == EXIT:
			break

if __name__ == '__main__':
	main()
