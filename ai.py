#!/usr/bin/python3

from board import Board

class AI():
	def __init__(self, currentBoard, player, depth=3):
		self.tree = self.getEmptyNode()
		self.tree["BOARD"] = currentBoard
		self.tree["PLAYER"] = player
		self.depth = depth
		self.queue = [self.tree]
		self.queue1 = [self.tree]

	def getEmptyNode(self):
		tree = {
			"BOARD": ""
			"PLAYER": ""
			"MOVE": ""
			"NEXTSTATE": []
		}
		return tree

	def run(self):
		self.createTree(self.tree, currentLevel=0)
		self.printTree(self)

	def createTree(self, currentLevel):
		while (len(self.queue) != 0 and currentLevel <= self.depth):
			currentNode = self.queue.pop(0)

			validMoves = currentNode["BOARD"].legalMoves()
			if (len(validMoves) == 0):
				continue

			for move in validMoves:
				newNode = self.getEmptyNode()
				newNode["BOARD"] = currentNode["BOARD"].updateBoard(move, currentNode["PLAYER"])
				newNode["PLAYER"] = 1 - currentNode["PLAYER"]
				newNode["MOVE"] = move
				currentNode["NEXTSTATE"].append(newNode)
				self.queue.append(newNode)
			currentLevel += 1

	def printTree(self):
		while (len(self.queue1) != 0):
			currentNode = self.queue1.pop(0)

			for node in currentNode["NEXTSTATE"]:
				node["BOARD"].printBoard()
				self.queue1.extend(node["NEXTSTATE"])
