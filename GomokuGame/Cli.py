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

    def Continue(self):
        while True:
            again = input('Do you want to again? Input Y or Ctrl+C exit!')
            if (again == 'Y'):
                self._clear_board()
                return True

    def Print_chessborad(self, borad):
        self._print_chessboard(borad)