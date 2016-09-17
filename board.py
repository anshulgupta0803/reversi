#!/usr/bin/python3

WHITE = 0
BLACK = 1
EMPTY = 2
# PIECE[WHITE] = "X"
# PIECE[BLACK] = "O"
# PIECE[EMPTY] = "."
PIECE=["X", "O", "."]

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
        for i in range(8):
            for j in range(8):
                if self.board[i][j] == WHITE:
                    print(PIECE[WHITE], end=" ")
                elif self.board[i][j] == BLACK:
                    print(PIECE[BLACK], end=" ")
                elif self.board[i][j] == EMPTY:
                    print(PIECE[EMPTY], end=" ")
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
        print("")

    def isBoardFull(self):
        if self.filledSquares == 64:
            return True
        else:
            return False
