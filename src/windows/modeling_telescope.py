import sys
from PyQt5.QtWidgets import *
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont, QIcon
from windows import style
# import style
import pandas as pd

# superherit from QMainWindow
class Window(QWidget):  
    def __init__(self, df):
        super().__init__()
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
    
    def mainDesign(self):
        self.title = QLabel('Tau225 Among Telescopes')
        self.table = QTableWidget()
        self.heatmap = QPushButton('Visualization')
    
    def setTable(self, df):
        self.table.setRowCount(len(df))
        self.table.setColumnCount(df.shape[1])

        self.columnList = df.columns
        self.indexList = df.index
        for i in range(df.shape[1]):
            self.table.setHorizontalHeaderItem(i, QTableWidgetItem(self.columnList[i]))
        for j in range(df.shape[0]):
            self.table.setVerticalHeaderItem(j, QTableWidgetItem(self.indexList[j]))
        
        for r in range(len(df)):        
            for c in range(df.shape[1]):
                self.table.setItem(r,c, QTableWidgetItem(str(round(df.iloc[r,c],2))))

    
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
        self.bottomLayout.addWidget(self.heatmap)
        ################# Setting Main Window Layout ########
        self.setLayout(self.mainLayout)
    
    def styles(self):
        self.title.setStyleSheet(style.single_tele_title())
    
        
    

  
def main():
    df = pd.read_csv('data/tau_df.csv', index_col = 0)
    App = QApplication(sys.argv)
    window = Window(df)
    sys.exit(App.exec_())

if __name__ == '__main__':
    main()