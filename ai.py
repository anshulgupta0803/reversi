#!/usr/bin/python3

from board import Board
import random

class AI():
	def __init__(self, currentBoard, depth=4):
		self.tree = self.getEmptyNode()
		self.tree["BOARD"] = currentBoard
		self.tree["MOVE"] = None
		self.tree["NEXTSTATE"] = []
		self.tree["LEVEL"] = 0
		self.depth = depth
		self.infinity = 1e50

	def getEmptyNode(self):
		tree = {
			"BOARD": None,
			"MOVE": None,
			"NEXTSTATE": None,
			"LEVEL": None,
			"BESTCHILD": None
		}
		return tree

	def run(self):
		self.createTree()
		# self.printTree()
		self.minimax(self.tree, self.depth, self.tree["BOARD"].myColor)
		return self.tree["BESTCHILD"]["MOVE"]

	def createTree(self):
		queue = [self.tree]
		while (len(queue) != 0):
			currentNode = queue.pop(0)
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
				queue.append(newNode)

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
		return 0

	def printTree(self):
		queue = [self.tree]
		while (len(queue) != 0):
			currentNode = queue.pop(0)
			if (currentNode["BOARD"] != None):
				print("LEVEL:", currentNode["LEVEL"])
				currentNode["BOARD"].printBoard()
				queue.extend(currentNode["NEXTSTATE"])
