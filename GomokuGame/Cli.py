import random
import numpy as np
import GomokuAI.Base as Base

class GomokuGameCLI(Base.BaseBoard):
    def __init__(self, size):
        super().__init__(size)

    def __print_winner(self, var):
        if var == 1:
            print('You win!')
        else:
            print('Com Win!')

    def Check_win(self, borad):
        for x in range(len(borad)):
            for y in range(len(borad)):
                if (borad[x][y] == 0):
                    continue
                if self._check_connected(borad, [x, y], 5):
                    self.__print_winner(borad[x][y])
                    return True
        return False

    def __clear_board(self):
        for i in range(self._BOARD_SIZE):
            for j in range(self._BOARD_SIZE):
                self._board[i][j] = 0

    def Continue(self):
        while True:
            again = input('Do you want to again? Input Y or Ctrl+C exit!')
            if (again == 'Y'):
                self.__clear_board()
                return True

    def Print_chessborad(self, borad):
        print("    ", end = "")
        for i in range(len(borad)):
            print(i, end = " ")
        print()

        for index, i in enumerate(borad):
            for j in range(0, len(i)):
                if j == 0:
                    print(index , "[ ", end="")
                print(i[j], end=" ")
                if j == len(i) - 1:
                    print("]", end="")
            print()