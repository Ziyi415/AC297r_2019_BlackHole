import sys
from PyQt5.QtWidgets import *
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont, QIcon
import mainPage
import style
import pandas as pd

# superherit from QMainWindow
class Window(QWidget):  
    def __init__(self,df):
        super().__init__()
        self.df = df
        self.setGeometry(240+600, 150, 590, 350) # Location(X,Y) and Size(X,Y) of the Window
        self.UI()
        self.setWindowTitle('Advanced Settings')
        self.show() # we need to show the window

    def UI(self):
        self.mainDesign()
        self.setTable()
        self.layouts()
        self.styles()   
    
    def mainDesign(self):
        self.title = QLabel('Baseline Length (km)')
        self.table = QTableWidget()
        self.add_btn = QPushButton('Add Telescope')
        self.update_btn = QPushButton('Update Database')

    def setTable(self):
        self.table.setRowCount(len(self.df))
        self.table.setColumnCount(len(self.df))
        self.columnList = self.df.columns
        for i in range(len(self.df)):
            self.table.setHorizontalHeaderItem(i, QTableWidgetItem(self.columnList[i]))
            self.table.setVerticalHeaderItem(i, QTableWidgetItem(self.columnList[i]))
        
        for r in range(len(self.df)):        
            for c in range(len(self.df)):
                self.table.setItem(r,c, QTableWidgetItem(str(self.df.iloc[r,c])))

    def layouts(self):
        ################## Layouts ########################
        self.mainLayout = QVBoxLayout()
        self.topLayout = QHBoxLayout()
        self.middleLayout = QHBoxLayout()
        self.bottomLayout = QHBoxLayout()
        ################# Adding Child Layouts #############
        self.mainLayout.addLayout(self.topLayout)
        self.mainLayout.addLayout(self.middleLayout)
        self.mainLayout.addLayout(self.bottomLayout)
        ################## Adding Widgets ###################
        self.topLayout.addStretch()
        self.topLayout.addWidget(self.title)
        self.topLayout.addStretch()
        self.middleLayout.addWidget(self.table)
        self.bottomLayout.addWidget(self.add_btn)
        self.bottomLayout.addWidget(self.update_btn)
        ################# Setting Main Window Layout ########
        self.setLayout(self.mainLayout)
    
    def styles(self):
        self.title.setStyleSheet(style.single_tele_title())
    




        
def main():
    App = QApplication(sys.argv)
    window = Window()
    sys.exit(App.exec_())

if __name__ == '__main__':
    main()