import sys
import PyQt5.QtWidgets as QtWidgets
import GomokuGame.Gui as Gui

if __name__ == '__main__':  
    app = QtWidgets.QApplication(sys.argv)  
    goBang = Gui.GomokuGUI()
    sys.exit(app.exec_())