import sys
from PyQt5.QtWidgets import *
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont, QIcon

class Window(QWidget):  
    def __init__(self):
        super().__init__()
        self.setGeometry(240+600, 150, 500, 100) # Location(X,Y) and Size(X,Y) of the Window
        self.UI()
        self.setWindowTitle('Advanced Settings')
        self.show() # we need to show the window
        

    def UI(self):
        self.mainDesign()
        self.layouts()
        self.styles()
        self.connections()
    
    def mainDesign(self):
        self.title_singleDiscount = QLabel('  Penalty Level for Single Discount Model: ')
        self.window_penalty_txt_singleDiscount = QLineEdit(self)
        self.window_penalty_txt_singleDiscount.setPlaceholderText("Non-Negative")

        self.title_furtherDiscount = QLabel('  Penalty Level for Further Discount Model: ')
        self.window_penalty_txt_furtherDiscount = QLineEdit(self)
        self.window_penalty_txt_furtherDiscount.setPlaceholderText("Non-Negative")

        self.title_thisTimeDiscount = QLabel('  Penalty Level for Uncertainty Today Model: ')
        self.window_penalty_txt_thisTimeDiscount = QLineEdit(self)
        self.window_penalty_txt_thisTimeDiscount.setPlaceholderText("Non-Negative")
        
        self.update_btn = QPushButton('Update', self)
        self.help_btn = QPushButton('?', self)

    def layouts(self):
        ################## Layouts ########################
        self.mainLayout = QVBoxLayout()
        self.topLayout = QFormLayout()
        self.bottomLayout = QHBoxLayout()
        ################# Adding Child Layouts #############
        # self.topLayout.addStretch()
        # self.topLayout.addStretch()
        self.mainLayout.addLayout(self.topLayout)
        self.mainLayout.addLayout(self.bottomLayout)
        ################## Adding Widgets ###################
        self.topLayout.addRow(self.title_singleDiscount, self.window_penalty_txt_singleDiscount)
        self.topLayout.addRow(self.title_furtherDiscount, self.window_penalty_txt_furtherDiscount)
        self.topLayout.addRow(self.title_thisTimeDiscount, self.window_penalty_txt_thisTimeDiscount)

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