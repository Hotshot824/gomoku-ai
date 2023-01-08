import GomokuSocket.Client as Client
import GomokuGame.Cli as Cli
import sys

if __name__ == '__main__':
    borad_size = 15
    borad = Cli.GomokuGameCLI(borad_size)
    client = Client.GomokuClient()

    borad.Print_chessborad(borad.Get_board())
    first = int(input("Who is first? (1):COM (2):Player"))
    while True:
        
        if first == 1:
            first = 2
            pass
        else:
            x, y = borad_size, borad_size
            while x >= borad_size or not(isinstance(x, int)):
                x = int(input("Please input x:"))
            while y >= borad_size or not(isinstance(y, int)):
                y = int(input("Please input y:"))
            borad.Place_chess(x, y)

        print('\033c', end='')
        borad.Print_chessborad(borad.Get_board())

        if borad.Check_win(borad.Get_board()):
            if borad.Continue():
                print('\033c', end='')
                borad.Print_chessborad(borad.Get_board())
                first = int(input("Who is first? (1):COM (2):Player"))
                pass
            else:
                sys.exit(0)
        else:
            data = {'chess_record': borad.Get_board()}
            client.connect()
            client.send_data(data)
            data = client.recv_data()
            borad.Place_chess_com(data['move'][0], data['move'][1])

            print('\033c', end='')
            borad.Print_chessborad(borad.Get_board())

            if borad.Check_win(borad.Get_board()):
                if borad.Continue():
                    print('\033c', end='')
                    borad.Print_chessborad(borad.Get_board())
                    first = int(input("Who is first? (1):COM (2):Player"))
                    pass
                else:
                    sys.exit(0)
    
