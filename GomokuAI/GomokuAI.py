import GomokuAI.Base as Base
import copy

class GomokuAI(Base.BaseBoard):
    def __init__(self):
        super().__init__()
        self.maxint = 2147483647
        self.minint = -2147483647
        self.__evaluate_table = self.__set_evaluate_table()
        self.__search_range = {'normal':[-1, 0, 1], 'hard':[-2, -1, 0, 1, 2]}
        self.__difficulty = self.Set_difficulty()
        self.__maxdepth = 4
        self.__inv_player = {1:2, 2:1}
        self.__count = 0

    def Get_count(self):
        return self.__count

    def Set_difficulty(self, config='normal'):
        return self.__search_range[config]

    def __set_evaluate_table(self):
        return {
            ('alive', 5) : self.maxint, ('death', 5) : self.maxint, ('close', 5) : self.maxint,
            ('alive', 4) : 100000, ('death', 4) : 1000, ('close', 4) : 0,
            ('alive', 3) : 1000, ('death', 3) : 100, ('close', 3) : 0,
            ('alive', 2) : 100, ('death', 2) : 10, ('close', 2) : 0,
            ('alive', 1) : 10, ('death', 1) : 1, ('close', 1) : 0,
        }

    def __piece_chess(self, board, position, player):
        tmp = copy.deepcopy(board)
        x, y = position[0], position[1]
        tmp[x][y] = player
        return tmp

    def __evaluate_role(self, board, role):
        value = 0
        for x in range(self._BOARD_SIZE):
            for y in range(self._BOARD_SIZE):
                if (board[x][y] != role):
                    continue
                for num in range(5, 1, -1):
                    result = self._check_connected(board, [x, y], num)
                    if result:
                        value += self.__evaluate_table[(result, num)]
                        continue
                result = self._check_single_chess(board, x, y, self.__inv_player[role])
                if result:
                    value += self.__evaluate_table[(result, 1)]
                    continue
        return value

    def __evaluate_board(self, board):
        return self.__evaluate_role(board, 2) - self.__evaluate_role(board, 1)

    # def __get_possible_moves(self, board):
    #     possible_moves = {}
    #     for i in range(self._BOARD_SIZE):
    #         for j in range(self._BOARD_SIZE):
    #             if board[i][j] == 0:
    #                 continue
    #             for x in self.__difficulty:
    #                 for y in self.__difficulty:
    #                     if x == 0 and y == 0:
    #                         continue
    #                     if i + x >= 0 and i + x < self._BOARD_SIZE and j + y >= 0 and j + y < self._BOARD_SIZE and board[i + x][j + y] == 0:
    #                         possible_moves[(i + x, j + y)] = True
    #     possible_moves = list(possible_moves.keys())
    #     return possible_moves

    def __get_possible_moves(self, board):
        possible_moves = {}
        for x in range(self._BOARD_SIZE):
            for y in range(self._BOARD_SIZE):
                if board[x][y] != 0:
                    continue
                if (x > 0 and board[x - 1][y] != 0) or \
                   (x < self._BOARD_SIZE - 1 and board[x + 1][y] != 0) or \
                   (y > 0 and board[x][y - 1] != 0) or \
                   (y < self._BOARD_SIZE - 1 and board[x][y + 1] != 0) or \
                   (x > 0 and y > 0 and board[x - 1][y - 1] != 0) or \
                   (x > 0 and y < self._BOARD_SIZE - 1 and board[x - 1][y + 1] != 0) or \
                   (x < self._BOARD_SIZE - 1 and y > 0 and board[x + 1][y - 1] != 0) or \
                   (x < self._BOARD_SIZE - 1 and y < self._BOARD_SIZE - 1 and board[x + 1][y + 1] != 0):
                    possible_moves[(x, y)] = True
        possible_moves = list(possible_moves.keys())
        return possible_moves

    def __sort_possible_move(self, board, possible_moves, player):
        tmp = {}
        for move in possible_moves:
            next_board = self.__piece_chess(board, [move[0], move[1]], player)
            value = self.__evaluate_board(next_board)
            tmp[(move[0], move[1])] = value
            if value > 10000:
                print(value, move)
                self.bestboard = next_board
                self.bestmove = move
                return [move]
        return sorted(tmp, key=tmp.get, reverse=True)

    # def minimax(self, board, depth, alpha, beta, maximizingPlayer):
    #     self.__count += 1
    #     if depth == 0 or self._game_over(board):
    #         value = self.__evaluate_board(board)
    #         return value, None, board

    #     if maximizingPlayer:
    #         max_score = self.minint
    #         best_move = None
    #         possible_moves = self.__get_possible_moves(board)
    #         # possible_moves = self.__sort_possible_move(board, possible_moves, 2)
    #         if depth == 4:
    #             print(possible_moves)
    #         for move in possible_moves:
    #             next_board = self.__piece_chess(board, [move[0], move[1]], 2)
    #             score, _, last_board = self.minimax(next_board, depth-1, alpha, beta, False)
    #             if score > max_score:
    #                 max_score = score
    #                 best_move =  move
    #                 best_board = last_board
    #             alpha = max(alpha, max_score)
    #             if beta < alpha:
    #                 break # beta cut-off
    #         return max_score, best_move, best_board

    #     else:
    #         min_score = self.maxint
    #         best_move = None
    #         possible_moves = self.__get_possible_moves(board)
    #         # possible_moves = self.__sort_possible_move(board, possible_moves, 2)
    #         for move in possible_moves:
    #             next_board = self.__piece_chess(board, [move[0], move[1]], 1)
    #             score, _, last_board = self.minimax(next_board, depth-1, alpha, beta, True)
    #             if score < min_score:
    #                 min_score = score
    #                 best_move =  move
    #                 best_board = last_board
    #             beta = min(beta, min_score)
    #             if beta < alpha:
    #                 break # alpha cut-off
    #         return min_score, best_move, best_board

    def __search(self, board, turn, depth, alpha, beta):
        self.__count += 1
        score = self.__evaluate_board(board)
        if depth <= 0 or self._game_over(board):
            return score

        possible_moves = self.__get_possible_moves(board)
        if depth == self.__maxdepth:
            possible_moves = self.__sort_possible_move(board, possible_moves, turn)
            print(possible_moves)
        bestmove = None

        # if there are no moves, just return the score
        if len(possible_moves) == 0:
            return score

        for move in possible_moves:
            x, y = move[0], move[1]
            board[x][y] = turn
            
            if turn == 2:
                op_turn = 1
            else:
                op_turn = 2

            score = - self.__search(board, op_turn, depth - 1, -beta, -alpha)

            board[x][y] = 0

            # alpha/beta pruning
            if score > alpha:
                alpha = score
                bestmove = (x, y)
                if alpha >= beta:
                    break

        if depth == self.maxdepth and bestmove:
            self.bestmove = bestmove
            self.bestboard = board
                    
        return alpha

    def minimax(self, board, depth, turn):
        self.maxdepth = depth
        self.bestmove = None
        self.bestboard = None
        score = self.__search(board, turn, self.__maxdepth, -2147483647, 2147483647)
        return score, self.bestmove, self.bestboard
