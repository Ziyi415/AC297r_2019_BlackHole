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
        self.mainDesign()
        self.layouts()
        self.styles()

    
    def mainDesign(self):
        self.title = QLabel('Suggested Action Path')
        self.decision_today_txt = QLabel('Decision 1st Day: ' )
        self.decision_today = QLabel('')
        
        self.decision_following_txt = QLabel('Following Days to Trigger: ')
        self.decision_following = QLabel('')

        self.CI_txt = QLabel('Level of Confidence: ')
        self.CI = QLabel('')


    def layouts(self):
        ################## Layouts ########################
        self.mainLayout = QVBoxLayout()
        self.topLayout = QHBoxLayout()
        self.middleLayout = QHBoxLayout()
        self.middleForm = QFormLayout()
        self.bottomLayout = QHBoxLayout()
        ################# Adding Child Layouts #############
        self.middleLayout.addStretch()
        self.middleLayout.addLayout(self.middleForm)
        self.middleLayout.addStretch()
        self.mainLayout.addLayout(self.topLayout)
        self.mainLayout.addLayout(self.middleLayout)
        self.mainLayout.addLayout(self.bottomLayout)
        ################## Adding Widgets ###################
        self.topLayout.addStretch()
        self.topLayout.addWidget(self.title)
        self.topLayout.addStretch()
        
        self.middleForm.addRow(self.decision_today_txt, self.decision_today)
        self.middleForm.addRow(self.decision_following_txt, self.decision_following)
        self.middleForm.addRow(self.CI_txt, self.CI)

        ################# Setting Main Window Layout ########
        self.setLayout(self.mainLayout)
    
    def styles(self):
        pass


        
def main():
    App = QApplication(sys.argv)
    window = Window()
    sys.exit(App.exec_())

if __name__ == '__main__':
    main()