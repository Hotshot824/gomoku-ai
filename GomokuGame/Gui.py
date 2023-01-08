import sys
import PyQt5.QtWidgets as QW
import GomokuAI.Base as Base
import GomokuSocket.Client as Client
import PyQt5.QtMultimedia as QM
import PyQt5.QtGui as QG
import PyQt5.QtCore as QC
import functools as ft


class GomokuGUI(QW.QWidget, Base.BaseBoard, Client.GomokuClient):
    def __init__(self):
        QW.QWidget.__init__(self)
        Base.BaseBoard.__init__(self)
        Client.GomokuClient.__init__(self)
        self.x = -1
        self.y = -1
        self.setWindowTitle('Gomoku Client')
        self.setFixedSize(660, 510)
        self.__game_state = ''
        self.__set_music()
        self.__set_start_btn()
        self.__set_restart_btn()
        self.__set_choose_btn()
        self.show()

    def __get_title_font(self):
        font = QG.QFont("Arial", 14)
        font.setBold(True)
        return font

    def __get_background_image(self):
        pixmap = QG.QPixmap('./image/background.jpg')
        brush = QG.QBrush(pixmap)
        return brush

    def __set_music(self):
        self.btn_sound = QM.QSound('./media/button.mp3')
        self.__playlist = QM.QMediaPlaylist()
        self.__playlist.addMedia(QM.QMediaContent(QC.QUrl.fromLocalFile("./media/background.mp3")))
        self.__playlist.setCurrentIndex(1)
        self.__playlist.setPlaybackMode(QM.QMediaPlaylist.PlaybackMode.CurrentItemInLoop)
        self.__music = QM.QMediaPlayer(self)
        self.__music.setPlaylist(self.__playlist)
        self.__music.setVolume(40)
        self.__music.setPlaybackRate(0.9)
        self.__music.play()

    def __set_start_btn(self):
        self.__start_btn = QW.QPushButton('Start Game', self)
        self.__start_btn.setGeometry(530, 170, 80, 40)
        self.__start_btn.setStyleSheet('''
            QPushButton {
                border:0;
                background-color:darkred;
                color:#fff;
                border-radius:10px;
            }
            QPushButton:hover {
                color:#003C9D;
                background-color:pink;
                border:2px #003C9D solid;
            }
        ''')
        self.__start_btn.clicked.connect(self.__click_start_btn_event)

    def __set_restart_btn(self):
        self.__restart_btn = QW.QPushButton('Restart', self)
        self.__restart_btn.setGeometry(530, 170, 80, 40)
        self.__restart_btn.setStyleSheet('''
            QPushButton {
                border:0;
                background-color:ForestGreen;
                color:#fff;
                border-radius:10px;
            }
            QPushButton:hover {
                color:#003C9D;
                background-color:LightGreen;
                border:2px #003C9D solid;
            }
        ''')
        self.__restart_btn.setVisible(False)

    def __set_choose_btn(self):
        choose_btn_style = '''
            QPushButton {
                border:0;
                background-color: dodgerblue;
                color:#fff;
                border-radius:10px;
            }
            QPushButton:hover {
                color:#003C9D;
                background-color:deepskyblue;
                border:10px #003C9D solid;
            }
        '''
        self.__choose_player_btn = QW.QPushButton('Player', self)
        self.__choose_player_btn.setGeometry(540, 160, 60, 30)
        self.__choose_player_btn.setStyleSheet(choose_btn_style)
        self.__choose_player_btn.setVisible(False)

        self.__choose_com_btn = QW.QPushButton('Computer', self)
        self.__choose_com_btn.setGeometry(540, 200, 60, 30)
        self.__choose_com_btn.setStyleSheet(choose_btn_style)
        self.__choose_com_btn.setVisible(False)

    def paintEvent(self, e):
        qp = QG.QPainter()
        qp.begin(self)
        qp.fillRect(self.rect(), self.__get_background_image())

        # paint chessboard
        qp.setPen(QG.QPen(QG.QColor(0, 0, 0), 2, QC.Qt.SolidLine))
        qp.drawRect(QC.QRect(50, 50, 420, 420))
        qp.setPen(QG.QPen(QG.QColor(0, 0, 0), 1, QC.Qt.SolidLine))
        for i in range(self._BOARD_SIZE):
            qp.drawLine(QC.QPoint(50, 50 + 30 * i),
                        QC.QPoint(470, 50 + 30 * i))
        for i in range(self._BOARD_SIZE):
            qp.drawLine(QC.QPoint(50 + 30 * i, 50),
                        QC.QPoint(50 + 30 * i, 470))

        qp.setFont(QG.QFont("Arial", 8))
        for i in range(self._BOARD_SIZE):
            num = i + 1
            qp.drawText(QC.QPoint(45 + 30 * i, 40), str(num))
            qp.drawText(QC.QPoint(30, 55 + 30 * i), str(num))

        # paint on chessboard five key point
        key_points = [(3, 3), (11, 3), (3, 11), (11, 11), (7, 7)]
        qp.setBrush(QG.QColor(0, 0, 0))
        for t in key_points:
            qp.drawEllipse(QC.QPoint(50 + 30 * t[0], 50 + 30 * t[1]), 3, 3)

        # paint black chess
        if len(self.__get_exist_chess(2)) != 0:
            for t in self.__get_exist_chess(2):
                qp.drawEllipse(QC.QPoint(50 + 30 * t[1], 50 + 30 * t[0]), 13, 13)

        # paint withe chess
        qp.setBrush(QG.QColor(255,255,255))
        if len(self.__get_exist_chess(1)) != 0:
            for t in self.__get_exist_chess(1):
                qp.drawEllipse(QC.QPoint(50 + 30 * t[1], 50 + 30 * t[0]), 13, 13)

        option = QG.QTextOption()
        option.setAlignment(QC.Qt.AlignHCenter)
        if self.__game_state == 'Choose':
            qp.setFont(self.__get_title_font())
            qp.drawText(QC.QRectF(470, 100, 200, 40), "Who is first?", option)
        if self.__game_state == 'Player':
            qp.setFont(self.__get_title_font())
            qp.drawText(QC.QRectF(470, 100, 200, 40), "Your Turn", option)
        if self.__game_state == 'Com':
            qp.setFont(self.__get_title_font())
            qp.drawText(QC.QRectF(470, 100, 200, 40), "Waiting...", option)

        qp.end()

    def __get_exist_chess(self, color):
        tmp = []
        for x in range(self._BOARD_SIZE):
            for y in range(self._BOARD_SIZE):
                if self._board[x][y] != color:
                    continue
                tmp.append((x, y))
        return tmp

    def __show_choose_btn(self, boolen):
        self.__choose_player_btn.setVisible(boolen)
        self.__choose_com_btn.setVisible(boolen)

    def __click_start_btn_event(self):
        self.btn_sound.play()
        self.__start_btn.setVisible(False)
        self.__show_choose_btn(True)
        self.__game_state = 'Choose'
        self.__choose_player_btn.clicked.connect(ft.partial(self.__click_start_game_event, 'player'))
        self.__choose_com_btn.clicked.connect(ft.partial(self.__click_start_game_event, 'com'))
        self.update()

    def __click_start_game_event(self, first):
        self.btn_sound.play()
        self.__show_choose_btn(False)
        self.__restart_btn.setVisible(True)
        if first == 'player':
            self.__game_state = 'Player'
        else:
            self.__game_state = 'Com'
        self.__restart_btn.clicked.connect(self.__click_restart_btn_event)
        self.update()

    def __click_restart_btn_event(self):
        self.btn_sound.play()
        self.__start_btn.setVisible(True)
        self.__restart_btn.setVisible(False)
        self.__game_state = ''
        self.__x = -1
        self.__y = -1
        self._clear_board()
        self.update()

    def mousePressEvent(self, e):
        if e.buttons() == QC.Qt.LeftButton:
            if e.x() > 15 and e.x() < 495 and e.y() > 15 and e.y() < 495:
                x = e.x()/30 - e.x()//30
                y = e.y()/30 - e.y()//30
                self.x = (e.y()-30)//30 if y < 0.5 else (e.y()-30)//30 + 1
                self.y = (e.x()-30)//30 if x < 0.5 else (e.x()-30)//30 + 1
                if self.__game_state == 'Player':
                    if self.put_white_chess(self.x - 1, self.y - 1):
                        print(self.x - 1, self.y - 1)
                        self._print_chessboard(self._board)

    #下白子
    def put_white_chess(self, x, y):
        if self._board[x][y] != 0:
            return False
        else:
            self._board[x][y] = 1
            self.update()
            return True
