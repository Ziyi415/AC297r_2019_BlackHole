import sys
from PyQt5.QtWidgets import *
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont, QIcon
import mainPage
import style
import pandas as pd

# superherit from QMainWindow
class Window(QWidget):  
    def __init__(self, df):
        super().__init__()
        self.df = df
        self.setGeometry(820-400, 150, 400, 350) # Location(X,Y) and Size(X,Y) of the Window
        self.UI()
        self.setWindowTitle('Advanced Settings')
        self.show() 

    def UI(self):
        self.mainDesign()
        self.setTable()
        self.layouts()
        self.connections()
        # self.styles()   
    
    def mainDesign(self):
        self.newTele_txt = QLabel('New Telescope Name:')
        self.newTele_line = QLineEdit(self)
        self.middle_txt = QLabel('Distance With Other Telescopes: ')
        self.table = QTableWidget()
        self.submit_btn = QPushButton('Submit', self)
        self.help_btn = QPushButton('?',self)


    def setTable(self):
        self.table.setRowCount(len(self.df))
        self.table.setColumnCount(1)
        self.columnList = ['Distance (km)']
        self.indexList = self.df.columns
        header = self.table.horizontalHeader()       
        header.setSectionResizeMode(0, QHeaderView.Stretch)
        self.table.setHorizontalHeaderItem(0, QTableWidgetItem('Distance (km)'))
        for i in range(len(self.indexList)):
            self.table.setVerticalHeaderItem(i, QTableWidgetItem('       ' + self.indexList[i]+ '       '))
    
    def writeTable(self):
        try:
            self.name = self.newTele_line.text()
            self.new_dist = []
            for r in range(self.table.rowCount()):
                self.new_dist.append(int(self.table.item(r,0).text()))
            
            self.df[self.name] = self.new_dist
            self.df = self.df.append(dict(zip(self.df.columns, self.new_dist+[0])), ignore_index = True)
            return self.df
        except:
            return self.df
    
        

    def layouts(self):
        ################## Layouts ########################
        self.mainLayout = QVBoxLayout()
        self.topLayout = QHBoxLayout()
        self.topLayoutLeft = QHBoxLayout()
        self.topLayoutRight = QHBoxLayout()
        self.middleLayout = QHBoxLayout()
        self.tableLayout = QHBoxLayout()
        self.submitLayout = QHBoxLayout()
        ################# Adding Child Layouts #############
        self.topLayout.addLayout(self.topLayoutLeft)
        self.topLayout.addLayout(self.topLayoutRight)
        self.mainLayout.addLayout(self.topLayout)
        self.mainLayout.addLayout(self.middleLayout)
        self.mainLayout.addLayout(self.tableLayout)
        self.mainLayout.addLayout(self.submitLayout)
        ################## Adding Widgets ###################
        self.topLayoutLeft.addWidget(self.newTele_txt)
        self.topLayoutRight.addWidget(self.newTele_line)
        self.middleLayout.addWidget(self.middle_txt)
        self.tableLayout.addWidget(self.table)
        self.submitLayout.addWidget(self.submit_btn,88)
        self.submitLayout.addWidget(self.help_btn,12)
        ################# Setting Main Window Layout ########
        self.setLayout(self.mainLayout)
    
    # def styles(self):
    #     self.title.setStyleSheet(style.single_tele_title())

    def connections(self):
        self.help_btn.clicked.connect(self.openHelp)
    
    def openHelp(self):
        self.text = '[New Telescope Name]\nenter a telescope name as a string.\n\n[Distance]\nplease enter the distance between telescopes in km as integer.'
        QMessageBox.information(self,'Information', self.text)            
    




        
def main():
    data = pd.read_csv('data/baseline_length_default.csv')
    App = QApplication(sys.argv)
    window = Window(data)
    sys.exit(App.exec_())

if __name__ == '__main__':
    main()