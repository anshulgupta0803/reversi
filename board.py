#!/usr/bin/python3

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

class Board():
	def __init__(self, myColor):
		self.myColor = myColor
		self.opponentColor = 1 - myColor
		self.board = list()
		for i in range(8):
			self.board.append([EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY])
		self.board[3][3] = WHITE
		self.board[3][4] = BLACK
		self.board[4][3] = BLACK
		self.board[4][4] = WHITE
		# score[WHITE] = 2
		# score[BLACK] = 2
		self.score = [2, 2]
		self.filledSquares = 4

	def printBoard(self):
		print("\n[INFO] Current board:")
		print("  ", end="")
		for i in range(8):
			print(i, end=" ")
		print("\n  ", end="")
		for i in range(8):
			print("_", end=" ")
		print("")
		for i in range(8):
			print(i, end="|")
			for j in range(8):
				if self.board[i][j] == WHITE:
					print(PIECE[WHITE], end="")
				elif self.board[i][j] == BLACK:
					print(PIECE[BLACK], end="")
				elif self.board[i][j] == EMPTY:
					print(PIECE[EMPTY], end="")
				if j == 7:
					print("|", end="")
				else:
					print(" ", end="")
				if i == 2 and j == 7:
					print("\tScoreboard:", end="")
				if i == 3 and j == 7:
					print("\tWhite", end="")
					if self.myColor == WHITE:
						print(" (You)", end="")
					print(": " + str(self.score[WHITE]), end="")
				if i == 4 and j == 7:
					print("\tBlack", end="")
					if self.myColor == BLACK:
						print(" (You)", end="")
					print(": " + str(self.score[BLACK]), end="")
			print("")
		print("  ", end="")
		for i in range(8):
			print("~", end=" ")
		print("")

	def getFinalScore(self):
		print("\nScoreboard:")
		print("White", end="")
		if self.myColor == WHITE:
			print(" (You)", end="")
		print(": " + str(self.score[WHITE]))
		print("Black", end="")
		if self.myColor == BLACK:
			print(" (You)", end="")
		print(": " + str(self.score[BLACK]))
		if self.score[self.myColor] > self.score[self.opponentColor]:
			print("\t\tYou Won!!")
		elif self.score[self.myColor] < self.score[self.opponentColor]:
			print("\t\tYou Lost!!")
		else:
			print("\t\tIt's a tie!!")

	def isBoardFull(self):
		if self.filledSquares == 64:
			return True
		else:
			return False

	def validateMove(self, move):
		if len(move) == 3:
			if move == str(EXIT):
				return EXIT
			if move == str(PASS):
				return PASS
			validMoves = self.legalMoves()
			try:
				validMoves.index(move)
				return move
			except Exception as e:
				return INVALID
		else:
			return INVALID

	def legalMoves(self):
		moves = list()
		for i in range(8):
			for j in range(8):
				if self.board[i][j] == self.myColor:


					# Check for vertical moves
					opponentPiecePresent = False
					for x in range(i - 1, -1, -1):
						if not(opponentPiecePresent) and self.board[x][j] == EMPTY:
							break
						if not(opponentPiecePresent) and self.board[x][j] == self.opponentColor:
							opponentPiecePresent = True
						if self.board[x][j] == self.myColor:
							break
						if opponentPiecePresent and self.board[x][j] == EMPTY:
							try:
								moves.index(str(x) + " " + str(j))
							except Exception as e:
								moves.append(str(x) + " " + str(j))
							opponentPiecePresent = False
							break
					opponentPiecePresent = False
					for x in range(i + 1, 8):
						if not(opponentPiecePresent) and self.board[x][j] == EMPTY:
							break
						if not(opponentPiecePresent) and self.board[x][j] == self.opponentColor:
							opponentPiecePresent = True
						if self.board[x][j] == self.myColor:
							break
						if opponentPiecePresent and self.board[x][j] == EMPTY:
							try:
								moves.index(str(x) + " " + str(j))
							except Exception as e:
								moves.append(str(x) + " " + str(j))
							opponentPiecePresent = False
							break

					# Check for horizontal moves
					opponentPiecePresent = False
					for y in range(j - 1, -1, -1):
						if not(opponentPiecePresent) and self.board[i][y] == EMPTY:
							break
						if not(opponentPiecePresent) and self.board[i][y] == self.opponentColor:
							opponentPiecePresent = True
						if self.board[i][y] == self.myColor:
							break
						if opponentPiecePresent and self.board[i][y] == EMPTY:
							try:
								moves.index(str(i) + " " + str(y))
							except Exception as e:
								moves.append(str(i) + " " + str(y))
							opponentPiecePresent = False
							break
					opponentPiecePresent = False
					for y in range(j + 1, 8):
						if not(opponentPiecePresent) and self.board[i][y] == EMPTY:
							break
						if not(opponentPiecePresent) and self.board[i][y] == self.opponentColor:
							opponentPiecePresent = True
						if self.board[i][y] == self.myColor:
							break
						if opponentPiecePresent and self.board[i][y] == EMPTY:
							try:
								moves.index(str(i) + " " + str(y))
							except Exception as e:
								moves.append(str(i) + " " + str(y))
							opponentPiecePresent = False
							break

					# Check for moves on main diagoanl
					opponentPiecePresent = False
					for p in range(1, 8):
						if i - p >= 0 and j - p >= 0:
							if not(opponentPiecePresent) and self.board[i - p][j - p] == EMPTY:
								break
							if not(opponentPiecePresent) and self.board[i - p][j - p] == self.opponentColor:
								opponentPiecePresent = True
							if self.board[i - p][j - p] == self.myColor:
								break
							if opponentPiecePresent and self.board[i - p][j - p] == EMPTY:
								try:
									moves.index(str(i - p) + " " + str(j - p))
								except Exception as e:
									moves.append(str(i - p) + " " + str(j - p))
								opponentPiecePresent = False
								break
						else:
							break
					opponentPiecePresent = False
					for p in range(1, 8):
						if i + p <= 7 and j + p <= 7:
							if not(opponentPiecePresent) and self.board[i + p][j + p] == EMPTY:
								break
							if not(opponentPiecePresent) and self.board[i + p][j + p] == self.opponentColor:
								opponentPiecePresent = True
							if self.board[i + p][j + p] == self.myColor:
								break
							if opponentPiecePresent and self.board[i + p][j + p] == EMPTY:
								try:
									moves.index(str(i + p) + " " + str(j + p))
								except Exception as e:
									moves.append(str(i + p) + " " + str(j + p))
								opponentPiecePresent = False
								break
						else:
							break

					# Check for moves on anti-diagonal
					opponentPiecePresent = False
					for p in range(1, 8):
						if i + p <= 7 and j - p >= 0:
							if not(opponentPiecePresent) and self.board[i + p][j - p] == EMPTY:
								break
							if not(opponentPiecePresent) and self.board[i + p][j - p] == self.opponentColor:
								opponentPiecePresent = True
							if self.board[i + p][j - p] == self.myColor:
								break
							if opponentPiecePresent and self.board[i + p][j - p] == EMPTY:
								try:
									moves.index(str(i + p) + " " + str(j - p))
								except Exception as e:
									moves.append(str(i + p) + " " + str(j - p))
								opponentPiecePresent = False
								break
						else:
							break
					opponentPiecePresent = False
					for p in range(1, 8):
						if i - p >= 0 and j + p <= 7:
							if not(opponentPiecePresent) and self.board[i - p][j + p] == EMPTY:
								break
							if not(opponentPiecePresent) and self.board[i - p][j + p] == self.opponentColor:
								opponentPiecePresent = True
							if self.board[i - p][j + p] == self.myColor:
								break
							if opponentPiecePresent and self.board[i - p][j + p] == EMPTY:
								try:
									moves.index(str(i - p) + " " + str(j + p))
								except Exception as e:
									moves.append(str(i - p) + " " + str(j + p))
								opponentPiecePresent = False
								break
						else:
							break
		return moves

	def updateBoard(self, move, color):
		i = int(move[:1])
		j = int(move[2:])
		self.board[i][j] = color
		self.filledSquares = self.filledSquares + 1
		self.score[color] = self.score[color] + 1

		# Check for vertical pieces
		potentialPieces = list()
		for x in range(i - 1, -1, -1):
			if self.board[x][j] == 1 - color:
				potentialPieces.append(str(x) + str(j))
			elif self.board[x][j] == color:
				for piece in potentialPieces:
					self.board[int(piece[:1])][int(piece[1:])] = color
					self.score[color] = self.score[color] + 1
					self.score[1 - color] = self.score[1 - color] - 1
				break
			elif self.board[x][j] == EMPTY:
				break
		potentialPieces = list()
		for x in range(i + 1, 8):
			if self.board[x][j] == 1 - color:
				potentialPieces.append(str(x) + str(j))
			elif self.board[x][j] == color:
				for piece in potentialPieces:
					self.board[int(piece[:1])][int(piece[1:])] = color
					self.score[color] = self.score[color] + 1
					self.score[1 - color] = self.score[1 - color] - 1
				break
			elif self.board[x][j] == EMPTY:
				break

		# Check for horizontal pieces
		potentialPieces = list()
		for y in range(j - 1, -1, -1):
			if self.board[i][y] == 1 - color:
				potentialPieces.append(str(i) + str(y))
			elif self.board[i][y] == color:
				for piece in potentialPieces:
					self.board[int(piece[:1])][int(piece[1:])] = color
					self.score[color] = self.score[color] + 1
					self.score[1 - color] = self.score[1 - color] - 1
				break
			elif self.board[i][y] == EMPTY:
				break
		potentialPieces = list()
		for y in range(j + 1, 8):
			if self.board[i][y] == 1 - color:
				potentialPieces.append(str(i) + str(y))
			elif self.board[i][y] == color:
				for piece in potentialPieces:
					self.board[int(piece[:1])][int(piece[1:])] = color
					self.score[color] = self.score[color] + 1
					self.score[1 - color] = self.score[1 - color] - 1
				break
			elif self.board[i][y] == EMPTY:
				break

		# Check for pieces on main diagoanl
		potentialPieces = list()
		for p in range(1, 8):
			if i - p >= 0 and j - p >= 0:
				if self.board[i - p][j - p] == 1 - color:
					potentialPieces.append(str(i - p) + str(j - p))
				elif self.board[i - p][j - p] == color:
					for piece in potentialPieces:
						self.board[int(piece[:1])][int(piece[1:])] = color
						self.score[color] = self.score[color] + 1
						self.score[1 - color] = self.score[1 - color] - 1
					break
				elif self.board[i - p][j - p] == EMPTY:
					break
			else:
				break
		potentialPieces = list()
		for p in range(1, 8):
			if i + p <= 7 and j + p <= 7:
				if self.board[i + p][j + p] == 1 - color:
					potentialPieces.append(str(i + p) + str(j + p))
				elif self.board[i + p][j + p] == color:
					for piece in potentialPieces:
						self.board[int(piece[:1])][int(piece[1:])] = color
						self.score[color] = self.score[color] + 1
						self.score[1 - color] = self.score[1 - color] - 1
					break
				elif self.board[i + p][j + p] == EMPTY:
					break
			else:
				break

		# Check for pieces on anti-diagonal
		potentialPieces = list()
		for p in range(1, 8):
			if i + p <= 7 and j - p >= 0:
				if self.board[i + p][j - p] == 1 - color:
					potentialPieces.append(str(i + p) + str(j - p))
				elif self.board[i + p][j - p] == color:
					for piece in potentialPieces:
						self.board[int(piece[:1])][int(piece[1:])] = color
						self.score[color] = self.score[color] + 1
						self.score[1 - color] = self.score[1 - color] - 1
					break
				elif self.board[i + p][j - p] == EMPTY:
					break
			else:
				break
		potentialPieces = list()
		for p in range(1, 8):
			if i - p >= 0 and j + p <= 7:
				if self.board[i - p][j + p] == 1 - color:
					potentialPieces.append(str(i - p) + str(j + p))
				elif self.board[i - p][j + p] == color:
					for piece in potentialPieces:
						self.board[int(piece[:1])][int(piece[1:])] = color
						self.score[color] = self.score[color] + 1
						self.score[1 - color] = self.score[1 - color] - 1
					break
				elif self.board[i - p][j + p] == EMPTY:
					break
			else:
				break
