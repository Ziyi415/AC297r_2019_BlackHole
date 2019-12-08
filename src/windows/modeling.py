import sys
from PyQt5.QtWidgets import *
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap, QFont, QIcon
# import style
from windows import style

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
        self.title = QLabel(self)
        self.pixmap = QPixmap('images/eht.png')
        self.sizedPixmap = self.pixmap.scaled(500,1024, Qt.KeepAspectRatio)
        self.title.setPixmap(self.sizedPixmap)
        self.decision_today_txt = QLabel('Decision 1st Day: ' )
        self.decision_today = QLabel('test')
        
        self.decision_following_txt = QLabel('Optimal Path to Trigger: ')
        self.decision_following = QLabel('test')

        self.CI_txt = QLabel('Level of Confidence: ')
        self.CI = QLabel('test')

        self.blank = QLabel(' ')

        self.decision_second_txt = QLabel('Second Optimal Path to Trigger: ')
        self.decision_second = QLabel('test')
        
        self.CI_second_txt = QLabel('Level of Confidence: ')
        self.CI_second = QLabel('test')



        self.model_comparison = QPushButton('Model Comparison', self)
        self.teles_comparison = QPushButton('Telescopes Comparison', self)


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
        self.middleForm.addRow(self.blank, self.blank)
        self.middleForm.addRow(self.decision_second_txt, self.decision_second)
        self.middleForm.addRow(self.CI_second_txt, self.CI_second)

        self.bottomLayout.addWidget(self.model_comparison)
        self.bottomLayout.addWidget(self.teles_comparison)
        ################# Setting Main Window Layout ########
        self.setLayout(self.mainLayout)
    
    def styles(self):

        self.decision_today_txt.setStyleSheet(style.model_label())
        self.decision_following_txt.setStyleSheet(style.model_label())
        self.CI_txt.setStyleSheet(style.model_label())
        self.decision_second_txt.setStyleSheet(style.model_label())
        self.CI_second_txt.setStyleSheet(style.model_label())

        self.decision_today.setStyleSheet(style.model_result())
        self.decision_following.setStyleSheet(style.model_result())
        self.CI.setStyleSheet(style.model_result())
        self.decision_second.setStyleSheet(style.model_result())
        self.CI_second.setStyleSheet(style.model_result())


        
def main():
    App = QApplication(sys.argv)
    window = Window()
    sys.exit(App.exec_())

if __name__ == '__main__':
    main()