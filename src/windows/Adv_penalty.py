import sys
from PyQt5.QtWidgets import *
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont, QIcon

class Window(QWidget):  
    def __init__(self):
        super().__init__()
        self.setGeometry(240+600, 150, 300, 100) # Location(X,Y) and Size(X,Y) of the Window
        self.UI()
        self.setWindowTitle('Advanced Settings')
        self.show() # we need to show the window
        

    def UI(self):
        self.mainDesign()
        self.layouts()
        self.styles()
        self.connections()
    
    def mainDesign(self):
        self.title = QLabel('  Penalty Level: ')
        self.window_penalty_txt = QLineEdit(self)
        self.window_penalty_txt.setPlaceholderText("Non-Negative")
        self.update_btn = QPushButton('Update', self)
        self.help_btn = QPushButton('?', self)

    def layouts(self):
        ################## Layouts ########################
        self.mainLayout = QVBoxLayout()
        self.topLayout = QHBoxLayout()
        self.topLayout_Right = QHBoxLayout()
        self.topLayout_Left = QHBoxLayout()
        self.bottomLayout = QHBoxLayout()
        ################# Adding Child Layouts #############
        # self.topLayout.addStretch()
        self.topLayout.addLayout(self.topLayout_Left)
        self.topLayout.addLayout(self.topLayout_Right)
        # self.topLayout.addStretch()
        self.mainLayout.addLayout(self.topLayout)
        self.mainLayout.addLayout(self.bottomLayout)
        ################## Adding Widgets ###################
        self.topLayout_Left.addWidget(self.title)
        self.topLayout_Right.addWidget(self.window_penalty_txt)
        # self.bottomLayout.addStretch()
        self.bottomLayout.addWidget(self.update_btn,83)
        self.bottomLayout.addWidget(self.help_btn,16)
        # self.bottomLayout.addStretch()
        ################# Setting Main Window Layout ########
        self.setLayout(self.mainLayout)

    
    def styles(self):
        pass

    def connections(self):
        self.help_btn.clicked.connect(self.openHelp)
    
    def openHelp(self):
        self.text = 'Enter a non-negative number as the penalty level.'
        QMessageBox.information(self,'Information', self.text)    

    

        
def main():
    App = QApplication(sys.argv)
    window = Window()
    sys.exit(App.exec_())

if __name__ == '__main__':
    main()