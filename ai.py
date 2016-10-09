#!/usr/bin/python3

from board import Board

class AI():
	def __init__(self, currentBoard, depth=4):
		self.tree = self.getEmptyNode()
		self.tree["BOARD"] = currentBoard
		self.tree["MOVE"] = None
		self.tree["NEXTSTATE"] = []
		self.tree["LEVEL"] = 0
		self.depth = depth
		self.queue = [self.tree]
		self.queue1 = [self.tree]

	def getEmptyNode(self):
		tree = {
			"BOARD": None,
			"MOVE": None,
			"NEXTSTATE": None,
			"LEVEL": None
		}
		return tree

	def run(self):
		self.createTree()
		# self.printTree()

	def createTree(self):
		while (len(self.queue) != 0):
			currentNode = self.queue.pop(0)
			if (currentNode["LEVEL"] > self.depth):
				break;

			try:
				validMoves = currentNode["BOARD"].legalMoves()
			except Exception as e:
				continue

			if (len(validMoves) == 0):
				continue

			for move in validMoves:
				newNode = self.getEmptyNode()

				if (currentNode["LEVEL"] < self.depth):
					clonedBoard = Board(currentNode["BOARD"].myColor)
					clonedBoard.score[0] = currentNode["BOARD"].score[0]
					clonedBoard.score[1] = currentNode["BOARD"].score[1]
					clonedBoard.filledSquares = currentNode["BOARD"].filledSquares
					clonedBoard.setState(currentNode["BOARD"].board)
					clonedBoard.updateBoard(move, currentNode["BOARD"].myColor)
					clonedBoard.myColor = 1 - currentNode["BOARD"].myColor
					clonedBoard.opponentColor = currentNode["BOARD"].myColor
				else:
					clonedBoard = None

				newNode["BOARD"] = clonedBoard
				newNode["MOVE"] = move
				newNode["NEXTSTATE"] = []
				newNode["LEVEL"] = currentNode["LEVEL"] + 1

				currentNode["NEXTSTATE"].append(newNode)
				self.queue.append(newNode)

	def printTree(self):
		while (len(self.queue1) != 0):
			currentNode = self.queue1.pop(0)
			if (currentNode["BOARD"] != None):
				print("LEVEL:", currentNode["LEVEL"])
				currentNode["BOARD"].printBoard()
				self.queue1.extend(currentNode["NEXTSTATE"])
