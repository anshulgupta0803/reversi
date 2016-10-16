#!/usr/bin/python3

from board import Board
import random

class AI():
	def __init__(self, currentBoard, depth=4):
		self.tree = self.getEmptyNode()
		self.tree["BOARD"] = currentBoard
		self.tree["MOVE"] = None
		self.tree["NEXTSTATE"] = []
		self.depth = depth
		self.infinity = 1e50
		self.bestMove = None
		self.createTree(self.tree, level=0)

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
		if (root == None or level > self.depth):
			return

		try:
			validMoves = root["BOARD"].legalMoves()
		except Exception as e:
			return

		if (len(validMoves) == 0):
			return

		for move in validMoves:
			newNode = self.getEmptyNode()

			if (level < self.depth):
				clonedBoard = Board(root["BOARD"].myColor)
				clonedBoard.score[0] = root["BOARD"].score[0]
				clonedBoard.score[1] = root["BOARD"].score[1]
				clonedBoard.filledSquares = root["BOARD"].filledSquares
				clonedBoard.setState(root["BOARD"].board)
				clonedBoard.updateBoard(move, root["BOARD"].myColor)
				clonedBoard.myColor = 1 - root["BOARD"].myColor
				clonedBoard.opponentColor = root["BOARD"].myColor
			elif (level == self.depth):
				clonedBoard = None

			newNode["BOARD"] = clonedBoard
			newNode["MOVE"] = move

			root["NEXTSTATE"].append(newNode)
			if (level == self.depth):
				self.tree["LASTLEVELNODES"].append(newNode)

			self.createTree(newNode, level + 1)

	def minimax(self, node, depth, player):
		if depth == 0 or node["NEXTSTATE"] == None:
			return self.heuristicValue(node)

		if (player == self.tree["BOARD"].myColor):
			bestValue = -1 * self.infinity
			for child in node["NEXTSTATE"]:
				v = self.minimax(child, depth - 1, 1 - player)
				if (bestValue < v):
					bestValue = v
					node["BESTCHILD"] = child
		else:
			bestValue = self.infinity
			for child in node["NEXTSTATE"]:
				v = self.minimax(child, depth - 1, 1 - player)
				if (bestValue > v):
					bestValue = v
					node["BESTCHILD"] = child
		return bestValue

	def heuristicValue(self, node):
		return random.randint(-100, 100)

	def think(self):
		self.minimax(self.tree, self.depth, self.tree["BOARD"].myColor)
		self.tree = self.tree["BESTCHILD"]
		print(self.tree["LASTLEVELNODES"])
		self.bestMove = self.tree["MOVE"]

	def getMove(self):
		return self.bestMove

	def printTree(self):
		queue = [self.tree]
		while (len(queue) != 0):
			currentNode = queue.pop(0)
			if (currentNode["BOARD"] != None):
				currentNode["BOARD"].printBoard()
				queue.extend(currentNode["NEXTSTATE"])
