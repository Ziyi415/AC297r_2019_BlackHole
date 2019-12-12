import sys
from PyQt5.QtWidgets import *
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont, QIcon, QPixmap
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
        self.icon = QLabel(self)
        self.pixmap = QPixmap('images/iacs.png')
        self.sizedPixmap = self.pixmap.scaled(50,50, Qt.KeepAspectRatio)
        self.icon.setPixmap(self.sizedPixmap)

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
        self.middleLayout = QHBoxLayout()
        self.middleRight = QFormLayout()
        self.middleRightLayout = QHBoxLayout()
        self.middleLeftLayout = QHBoxLayout()
        self.bottomLayout = QHBoxLayout()
        ################# Adding Child Layouts #############
        
        self.middleRightLayout.addLayout(self.middleRight)
        self.middleRightLayout.addStretch()
        self.middleLayout.addStretch()
        self.middleLayout.addLayout(self.middleLeftLayout)
        self.middleLayout.addLayout(self.middleRightLayout)
        self.middleLayout.addStretch()
        self.mainLayout.addLayout(self.titleLayout)
        self.mainLayout.addLayout(self.middleLayout)
        self.mainLayout.addLayout(self.bottomLayout)
        ################## Adding Widgets ###################
        self.titleLayout.addStretch()
        self.titleLayout.addWidget(self.title)
        self.titleLayout.addStretch()
        self.middleLeftLayout.addStretch()
        self.middleLeftLayout.addWidget(self.icon)
        self.middleLeftLayout.addStretch()
        self.middleRight.addRow(self.title_yiming, self.window_yiming)
        self.middleRight.addRow(self.title_shu, self.window_shu)
        self.middleRight.addRow(self.title_ziyi, self.window_ziyi)

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