import sys
from PyQt5.QtWidgets import *
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont, QIcon
# import style
from windows import style

class Window(QWidget):  
    def __init__(self):
        super().__init__()
        self.setGeometry(240+600, 150, 500, 100) # Location(X,Y) and Size(X,Y) of the Window
        self.UI()
        self.setWindowTitle('More Information')
        self.show() # we need to show the window
        

    def UI(self):
        self.mainDesign()
        self.layouts()
        self.styles()
    
    def mainDesign(self):
        self.title = QLabel('Contact Us')
        self.title_yiming = QLabel('  Yiming Xu: ')
        self.window_yiming = QLabel('yimingxu@g.harvard.edu')

        self.title_shu = QLabel('  Shu Xu: ')
        self.window_shu = QLabel('shuxu@g.harvard.edu')

        self.title_ziyi = QLabel('  Ziyi Zhou: ')
        self.window_ziyi = QLabel('ziyi_zhou@g.harvard.edu')

    def layouts(self):
        ################## Layouts ########################
        self.mainLayout = QVBoxLayout()
        self.titleLayout = QHBoxLayout()
        self.topLayout = QFormLayout()
        self.bottomLayout = QHBoxLayout()
        ################# Adding Child Layouts #############
        # self.topLayout.addStretch()
        # self.topLayout.addStretch()
        self.mainLayout.addLayout(self.titleLayout)
        self.mainLayout.addLayout(self.topLayout)
        self.mainLayout.addLayout(self.bottomLayout)
        ################## Adding Widgets ###################
        self.titleLayout.addStretch()
        self.titleLayout.addWidget(self.title)
        self.titleLayout.addStretch()
        self.topLayout.addRow(self.title_yiming, self.window_yiming)
        self.topLayout.addRow(self.title_shu, self.window_shu)
        self.topLayout.addRow(self.title_ziyi, self.window_ziyi)

        ################# Setting Main Window Layout ########
        self.setLayout(self.mainLayout)

    
    def styles(self):
        self.title.setStyleSheet(style.contact_title())

    
  

def main():
    App = QApplication(sys.argv)
    window = Window()
    sys.exit(App.exec_())

if __name__ == '__main__':
    main()