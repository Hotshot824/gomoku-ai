import random
import asyncio
import numpy as np


class BaseBoard():
    def __init__(self, size = 15):
        self._BOARD_SIZE = size
        self._board = [[0 for _ in range(self._BOARD_SIZE)] for _ in range(self._BOARD_SIZE)]
        self.__live_state = {0: "close", 1: "death", 2: "alive"}

    def Set_board(self, board):
        self._board = board
        self._BOARD_SIZE = len(board)

    def Get_board(self):
        return self._board

    def Place_chess(self, x, y):
        self._board[x][y] = 1

    def Place_chess_com(self, x, y):
        self._board[x][y] = 2
        
    def Is_board_empty(self):
        for x in self._board:
            for y in x:
                if y != 0:
                    return False
        return True

    def _clear_board(self):
        self._board = [[0 for _ in range(self._BOARD_SIZE)] for _ in range(self._BOARD_SIZE)]

    def Get_center_move(self):
        center = self._BOARD_SIZE // 2
        return (center + random.randint(-2, 2), center + random.randint(-2, 2))

    def _print_chessboard(self, board):
        # 顯示欄的標號
        print("    ", end="")
        for i in range(len(board)):
                print(f"{hex(i)[2:]:2}", end="")
        print()

        # 顯示棋盤
        for i, row in enumerate(board):
            print(f"{hex(i)[2:]:2}[", end="")
            for j in range(len(row)):
                print(f"{row[j]:>2}", end="")
                if j == len(row) - 1:
                    print(" ]", end="")
            print()

    def _game_over(self, borad):
        for x in range(self._BOARD_SIZE):
            for y in range(self._BOARD_SIZE):
                if (borad[x][y] == 0):
                    continue
                if self._check_connected(borad, [x, y], 5):
                    return True
        return False

    def __check_alive(self, board, x, y, direction, num):
        state = 0
        if direction == (0, 1):
            if y+num < len(board):
                if board[x][y+num] == 0:
                    state += 1
            if y-1 >= 0:
                if board[x][y-1] == 0:
                    state += 1
            return self.__live_state[state]
        if direction == (1, 0):
            if x+num < len(board):
                if board[x+num][y] == 0:
                    state += 1
            if x-1 >= 0:
                if board[x-1][y] == 0:
                    state += 1
            return self.__live_state[state]
        if direction == (1, 1):
            if x+num < len(board) and y+num < len(board):
                if board[x+num][y+num] == 0:
                    state += 1
            if x-1 >= 0 and y-1 >= 0:
                if board[x-1][y-1] == 0:
                    state += 1
            return self.__live_state[state]
        if direction == (-1, 1):
            if x-num >= 0 and y+num < len(board):
                if board[x-num][y+num] == 0:
                    state += 1
            if x+1 < len(board) and y-1 >= 0:
                if board[x+1][y-1] == 0:
                    state += 1
            return self.__live_state[state]

    def __check_line(self, board, x, y, direction, origin):
        dx, dy = direction[0], direction[1]
        count = 1
        while True:
            x += dx
            y += dy
            if x < 0 or x >= len(board) or y < 0 or y >= len(board[0]):
                break
            if board[x][y] != origin:
                break
            count += 1
        return count

    def _check_connected(self, board, position, num):
        directions = [(1, 0), (0, 1), (1, 1), (-1, 1)]
        x, y = position[0], position[1]
        origin = board[x][y]
        for direction in directions:
            count = self.__check_line(board, x, y, direction, origin)
            if count == num:
                return self.__check_alive(board, x, y, direction, num)
        return False

    def _check_single_chess(self, board, x, y, role):
        if (x+1 < self._BOARD_SIZE and y+1 < self._BOARD_SIZE and x-1 >= 0 and y-1 >= 0):
            if (board[x][y+1] == board[x+1][y] == board[x][y-1] == board[x+1][y] ==
                    board[x+1][y+1] == board[x-1][y+1] == board[x+1][y-1] == board[x-1][y-1] == role):
                return 'alive'
            return 'death'
        else:
            return 'close'
