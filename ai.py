#!/usr/bin/python3

from board import Board
import gc	# For garbage collection
import threading

WHITE = 0
BLACK = 1
EMPTY = 2
# PIECE[WHITE] = "⚪"
# PIECE[BLACK] = "⏺"
# PIECE[EMPTY] = "∙"
PIECE = [u"\u26AA", u"\u23FA", u"\u2219"]

EXIT = 100
INVALID = -10
PASS = -20

class AI():
	def __init__(self, currentBoard, depth=4):
		self.tree = self.getEmptyNode()
		self.tree["BOARD"] = currentBoard
		self.depth = depth
		self.infinity = 1e50
		self.bestMove = None
		# To store the LASTLEVELNODES for this node
		#self.secondLevelParent = None
		self.count = 0
		self.createTree(self.tree, level=0)
		gc.enable()

	def getEmptyNode(self):
		tree = {
			"BOARD": None,
			"MOVE": None,
			"NEXTSTATE": list(),
			"LASTLEVELNODES": list(),
			"BESTCHILD": None
		}
		return tree

	def createTree(self, root, level):
		if root == None or level > self.depth:
			return

		try:
			validMoves = root["BOARD"].legalMoves()
		except Exception as e:
			return

		if len(validMoves) == 0:
			return

		#print("LEVEL:", level)
		if level == 2:
			#print("Added", self.count, "nodes in last level nodes for move", root["MOVE"])
			#self.secondLevelParent = root
			self.count = 0

		threads = list()
		for move in validMoves:
			newNode = self.getEmptyNode()

			#if level < self.depth:
			clonedBoard = Board(root["BOARD"].myColor)
			clonedBoard.score[0] = root["BOARD"].score[0]
			clonedBoard.score[1] = root["BOARD"].score[1]
			clonedBoard.filledSquares = root["BOARD"].filledSquares
			clonedBoard.setState(root["BOARD"].board)
			clonedBoard.updateBoard(move, root["BOARD"].myColor)
			clonedBoard.myColor = 1 - root["BOARD"].myColor
			clonedBoard.opponentColor = root["BOARD"].myColor
			#elif level == self.depth:
			#	clonedBoard = None

			newNode["BOARD"] = clonedBoard
			newNode["MOVE"] = move

			root["NEXTSTATE"].append(newNode)
			if level == self.depth:
				self.count += 1
				#self.secondLevelParent["LASTLEVELNODES"].append(newNode)

			self.createTree(newNode, level + 1)
			'''thread = threading.Thread(target=self.createTree, args=(newNode, level + 1))
			thread.start()
			threads.append(thread)

		for thread in threads:
			thread.join()'''

	def minimax(self, node, depth, player, alpha, beta):
		if depth == 0 or node["NEXTSTATE"] == None:
			return self.heuristicValue(node)

		if player == self.tree["BOARD"].myColor:		# Maximizer
			currentValue = -1 * self.infinity
			for child in node["NEXTSTATE"]:
				if currentValue < beta:					# Beta Pruning
					childValue = self.minimax(child, depth - 1, 1 - player, currentValue, beta)
					if currentValue < childValue:
						currentValue = childValue
						node["BESTCHILD"] = child
		else:											# Minimizer
			currentValue = self.infinity
			for child in node["NEXTSTATE"]:
				if currentValue > alpha:				# Alpha Pruning
					childValue = self.minimax(child, depth - 1, 1 - player, alpha, currentValue)
					if currentValue > childValue:
						currentValue = childValue
						node["BESTCHILD"] = child

		return currentValue

	def heuristicValue(self, node):
		diskSquares, pieceValue, frontierValue = self.pieceCount(node["BOARD"])
		cornerValue = self.cornerOccupancy(node["BOARD"])
		cornerClosenessValue = self.cornerCloseness(node["BOARD"])
		mobilityValue = self.mobility(node["BOARD"])
		return (10 * diskSquares) + (10 * pieceValue) + (74.396 * frontierValue) + (801.724 * cornerValue) + (382.026 * cornerClosenessValue) + (78.922 * mobilityValue)

	def cornerOccupancy(self, board):
		myPieces = 0
		opponentPieces = 0
		if board.board[0][0] == board.myColor:
			myPieces += 1
		elif board.board[0][0] == board.opponentColor:
			opponentPieces += 1

		if board.board[0][7] == board.myColor:
			myPieces += 1
		elif board.board[0][7] == board.opponentColor:
			opponentPieces += 1

		if board.board[7][0] == board.myColor:
			myPieces += 1
		elif board.board[7][0] == board.opponentColor:
			opponentPieces += 1

		if board.board[7][7] == board.myColor:
			myPieces += 1
		elif board.board[7][7] == board.opponentColor:
			opponentPieces += 1

		return 25 * (myPieces - opponentPieces)

	def cornerCloseness(self, board):
		myPieces = 0
		opponentPieces = 0

		if board.board[0][0] == EMPTY:
			if board.board[0][1] == board.myColor:
				myPieces += 1
			elif board.board[0][1] == board.opponentColor:
				opponentPieces += 1

			if board.board[1][0] == board.myColor:
				myPieces += 1
			elif board.board[1][0] == board.opponentColor:
				opponentPieces += 1

			if board.board[1][1] == board.myColor:
				myPieces += 1
			elif board.board[1][1] == board.opponentColor:
				opponentPieces += 1

		if board.board[0][7] == EMPTY:
			if board.board[0][6] == board.myColor:
				myPieces += 1
			elif board.board[0][6] == board.opponentColor:
				opponentPieces += 1

			if board.board[1][7] == board.myColor:
				myPieces += 1
			elif board.board[1][7] == board.opponentColor:
				opponentPieces += 1

			if board.board[1][6] == board.myColor:
				myPieces += 1
			elif board.board[1][6] == board.opponentColor:
				opponentPieces += 1

		if board.board[7][0] == EMPTY:
			if board.board[7][1] == board.myColor:
				myPieces += 1
			elif board.board[7][1] == board.opponentColor:
				opponentPieces += 1

			if board.board[6][0] == board.myColor:
				myPieces += 1
			elif board.board[6][0] == board.opponentColor:
				opponentPieces += 1

			if board.board[6][1] == board.myColor:
				myPieces += 1
			elif board.board[6][1] == board.opponentColor:
				opponentPieces += 1

		if board.board[7][7] == EMPTY:
			if board.board[6][7] == board.myColor:
				myPieces += 1
			elif board.board[6][7] == board.opponentColor:
				opponentPieces += 1

			if board.board[7][6] == board.myColor:
				myPieces += 1
			elif board.board[7][6] == board.opponentColor:
				opponentPieces += 1

			if board.board[6][6] == board.myColor:
				myPieces += 1
			elif board.board[6][6] == board.opponentColor:
				opponentPieces += 1

		return -12.5 * (myPieces - opponentPieces)

	def mobility(self, board):
		# Get my moves
		myMoves = len(board.legalMoves())

		# Get oppponent's moves
		board.myColor = 1 - board.myColor
		board.opponentColor = 1 - board.opponentColor
		opponentMoves = len(board.legalMoves())
		board.myColor = 1 - board.myColor
		board.opponentColor = 1 - board.opponentColor

		if myMoves > opponentMoves:
			return (100 * myMoves) / (myMoves + opponentMoves)
		elif myMoves < opponentMoves:
			return (-100 * opponentMoves) / (myMoves + opponentMoves)
		else:
			return 0

	def pieceCount(self, board):
		V = list()
		V.append([20, -3, 11, 8, 8, 11, -3, 20])
		V.append([-3, -7, -4, 1, 1, -4, -7, -3])
		V.append([11, -4, 2, 2, 2, 2, -4, 11])
		V.append([8, 1, 2, -3, -3, 2, 1, 8])
		V.append([8, 1, 2, -3, -3, 2, 1, 8])
		V.append([11, -4, 2, 2, 2, 2, -4, 11])
		V.append([-3, -7, -4, 1, 1, -4, -7, -3])
		V.append([20, -3, 11, 8, 8, 11, -3, 20])

		neighbor = [	(-1, -1),	(0, -1)	,	(1, -1),
						(-1, 0),				(1, 0),
						(-1, 1),	(0, 1),		(1, 1)	]

		#
		myPieces = 0
		opponentPieces = 0
		diskSquares = 0
		# Pieces which are on the perimeter
		myFrontierPieces = 0
		opponentFrontierPieces = 0
		for i in range(0, 8):
			for j in range(0, 8):
				if board.board[i][j] == board.myColor:
					diskSquares += V[i][j]
					myPieces += 1

				elif board.board[i][j] == board.opponentColor:
					diskSquares -= V[i][j]
					opponentPieces += 1

				if board.board[i][j] != EMPTY:
					for k in range(0, 8):
						x = i + neighbor[k][0]
						y = j + neighbor[k][1]
						if x >= 0 and x < 8 and y >= 0 and y < 8 and board.board[x][y] == EMPTY:
							if board.board[i][j] == board.myColor:
								myFrontierPieces += 1
							else:
								opponentFrontierPieces += 1
							break

		if myFrontierPieces > opponentFrontierPieces:
			frontierValue = (-100 * myFrontierPieces) / (myFrontierPieces + opponentFrontierPieces)
		elif myFrontierPieces < opponentFrontierPieces:
			frontierValue = (100 * opponentFrontierPieces) / (myFrontierPieces + opponentFrontierPieces)
		else:
			frontierValue = 0

		if myPieces > opponentPieces:
			pieceValue = (100 * myPieces) / (myPieces + opponentPieces)
		elif myPieces < opponentPieces:
			pieceValue = (-100 * myPieces) / (myPieces + opponentPieces)
		else:
			pieceValue = 0

		return (diskSquares, pieceValue, frontierValue)

	def think(self):
		self.minimax(self.tree, self.depth, self.tree["BOARD"].myColor, -1 * self.infinity, self.infinity)
		try:
			self.bestMove = self.tree["BESTCHILD"]["MOVE"]
		except Exception as e:
			print("Best Child is None")
			self.bestMove = self.tree["BOARD"].legalMoves()[0]

		self.tree = self.tree["BESTCHILD"]

	def observe(self, opponentMove):
		for child in self.tree["NEXTSTATE"]:
			if child["MOVE"] == opponentMove.strip("\n"):
				print("Found the child")
				self.tree = child
				break
		print("Processing last level nodes:", len(self.tree["LASTLEVELNODES"]))
		for lastLevelNode in self.tree["LASTLEVELNODES"]:
			self.createTree(lastLevelNode, 0)

	def getMove(self):
		return self.bestMove

	def printTree(self):
		queue = [self.tree]
		while len(queue) != 0:
			currentNode = queue.pop(0)
			if currentNode["BOARD"] != None:
				currentNode["BOARD"].printBoard()
				queue.extend(currentNode["NEXTSTATE"])
