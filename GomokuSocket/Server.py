import asyncio
import json, time
import GomokuAI.GomokuAI as GomokuAI


class GomokuServer(asyncio.Protocol, GomokuAI.GomokuAI):
    def connection_made(self, transport):
        asyncio.Protocol.__init__(self)
        GomokuAI.GomokuAI.__init__(self)
        self.__transport = transport
        self.__address = transport.get_extra_info('peername')
        print('Accepted connection from {}'.format(self.__address))

    def data_received(self, data):
        data = json.loads(data.decode("utf-8"))

        response = self.__parse(data)
        response = json.dumps(response)
        self.__transport.write(response.encode("utf-8"))
        # self.transport.close()

    def connection_lost(self, exc):
        if exc:
            print('client {} error: {}'.format(self.__address, exc))
        else:
            print('client {} closed socket'.format(self.__address))

    def __parse(self, require):
        if (require['chess_record']):
            # self._print_chessboard(require['chess_record'])
            self.Set_board(require['chess_record'])
            start = time.perf_counter()
            if self.Is_board_empty():
                move = self.Get_center_move()
                score, best_board = 0, require['chess_record']
            else:
                # score, move, best_board = self.minimax(require['chess_record'], 4, self.minint, self.maxint, True)
                score, move, best_board = self.minimax(require['chess_record'], 4, 2)
            end = time.perf_counter()
            print("best score: {}, best move: {}.".format(score, move))
            print("elapsed time: {:.6f}s, recursion times: {}.".format(end - start, self.Get_count()))
            self._print_chessboard(best_board)
            # score, move = self.test(require['chess_record'])
            response = {'score': score, 'move': move}
        return response

def RunServer():
    address = ("127.0.0.1", 4000)
    loop = asyncio.get_event_loop()
    coro = loop.create_server(GomokuServer, *address)
    server = loop.run_until_complete(coro)
    print('Listening at {}'.format(address))
    try:
        loop.run_forever()
    finally:
        server.close()
        loop.close()
