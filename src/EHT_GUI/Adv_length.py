import sys
from PyQt5.QtWidgets import *
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont, QIcon
import Adv_length_addTele, style
import pandas as pd
import numpy as np

# superherit from QMainWindow
class Window(QWidget):  
    def __init__(self,df):
        super().__init__()
        self.df_default = df
        self.df = df
        self.setGeometry(240+600, 150, 590, 350) # Location(X,Y) and Size(X,Y) of the Window
        self.UI()
        self.setWindowTitle('Advanced Settings')
        self.show() 

    def UI(self):
        self.mainDesign()
        self.setTable(self.df)
        self.layouts()
        self.styles()
        self.connections()   
    
    def mainDesign(self):
        self.title = QLabel('Baseline Length (km)')
        self.table = QTableWidget()
        self.reset_btn = QPushButton('Reset')
        self.add_btn = QPushButton('Add Telescope')
        self.update_btn = QPushButton('Update Database')
        self.help_btn = QPushButton('?')

    def setTable(self, df):
        self.table.setRowCount(len(df))
        self.table.setColumnCount(len(df))
        self.columnList = df.columns
        for i in range(len(df)):
            self.table.setHorizontalHeaderItem(i, QTableWidgetItem(self.columnList[i]))
            self.table.setVerticalHeaderItem(i, QTableWidgetItem(self.columnList[i]))
        
        for r in range(len(df)):        
            for c in range(len(df)):
                self.table.setItem(r,c, QTableWidgetItem(str(df.iloc[r,c])))
    
    def writeDf(self):
        self.values = []
        for r in range(self.table.rowCount()):
            for c in range(self.table.columnCount()):
                self.values.append(int(self.table.item(r, c).text()))
        self.df_new = pd.DataFrame(np.array(self.values).reshape(self.table.rowCount(), self.table.columnCount()))
        self.df_new.columns = self.df.columns
        return self.df_new

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
        self.bottomLayout.addWidget(self.reset_btn, 12)
        self.bottomLayout.addWidget(self.add_btn, 40)
        self.bottomLayout.addWidget(self.update_btn, 40)
        self.bottomLayout.addWidget(self.help_btn, 8)
        ################# Setting Main Window Layout ########
        self.setLayout(self.mainLayout)
    
    def styles(self):
        self.title.setStyleSheet(style.single_tele_title())
    
    def connections(self):
        self.add_btn.clicked.connect(self.openAddTele)
        self.reset_btn.clicked.connect(self.resetTable)
        self.help_btn.clicked.connect(self.openHelp)
    

    ############### Add Telescope Connections #########
    def openAddTele(self):
        self.run_addTele = Adv_length_addTele.Window(self.df)
        self.run_addTele.submit_btn.clicked.connect(self.updateBaselineDisplay)
    
    def updateBaselineDisplay(self):
        self.df = self.run_addTele.writeTable()
        self.setTable(self.df)
        self.run_addTele.close()
    
    def resetTable(self):
        self.setTable(self.df_default)
    
    def openHelp(self):
        self.text = '[Reset]\nreset the table to the default one.\n\n[Add Telescope]\nadd a new telescope, you will have to enter its distance from the other telescopes as well.\n\n[Update Database]\nuse this edited table as the default in the future as well.'
        QMessageBox.information(self,'Information', self.text)



        
def main():
    data = pd.read_csv('data/baseline_length_default.csv')
    App = QApplication(sys.argv)
    window = Window(data)
    sys.exit(App.exec_())

if __name__ == '__main__':
    main()