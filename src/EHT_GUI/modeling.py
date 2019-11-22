import sys
from PyQt5.QtWidgets import *
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont, QIcon

# superherit from QMainWindow
class Window(QWidget):  
    def __init__(self):
        super().__init__()
        self.setGeometry(240+600, 150, 500, 350) # Location(X,Y) and Size(X,Y) of the Window
        self.UI()
        self.setWindowTitle('Model Results')
        self.show() # we need to show the window

    def UI(self):
        return

    

        
def main():
    App = QApplication(sys.argv)
    window = Window()
    sys.exit(App.exec_())

if __name__ == '__main__':
    main()