import sys
import PyQt5.QtWidgets as QtWidgets
import GomokuGame.Gui as Gui

#程序入口
if __name__ == '__main__':  
    app = QtWidgets.QApplication(sys.argv)  
    goBang = Gui.GomokuGUI()
    sys.exit(app.exec_())