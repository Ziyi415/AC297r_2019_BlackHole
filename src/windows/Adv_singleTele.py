import sys
from PyQt5.QtWidgets import *
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont, QIcon
from windows import style
import pandas as pd

# superherit from QMainWindow
class Window(QWidget):  
    def __init__(self, df, df_default):
        super().__init__()
        self.df = df
        self.df_default = df_default
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
        self.title = QLabel('Single Telescope Information')
        self.table = QTableWidget()
        self.add_btn = QPushButton('Add')
        self.remove_btn = QPushButton('Remove')
        self.reset_btn = QPushButton('Reset')
        self.update_this_time = QPushButton('Update This Time')
        self.update_as_default = QPushButton('Update as Default')
        self.help_btn = QPushButton('?')
    
    def setTable(self, df):
        self.table.setRowCount(len(df))
        self.table.setColumnCount(4)
        header = self.table.horizontalHeader()       
        header.setSectionResizeMode(0, QHeaderView.Stretch)
        header.setSectionResizeMode(1, QHeaderView.ResizeToContents)
        header.setSectionResizeMode(2, QHeaderView.ResizeToContents)


        self.columnList = ['Name', 'Start Time', 'End Time', 'Weight']
        for i in range(4):
            self.table.setHorizontalHeaderItem(i, QTableWidgetItem(self.columnList[i]))
        
        for r in range(len(df)):        
            for c in range(4):
                self.table.setItem(r,c, QTableWidgetItem(str(df.iloc[r,c])))

    def writeDf(self):
        self.new_name = []
        self.new_start = []
        self.new_end = []
        self.new_weight = []
        self.new_avail = []
        for r in range(self.table.rowCount()):
            for c in range(4):
                if c == 0:
                    self.new_name.append(self.table.item(r, c).text())
                elif c == 1:
                    self.new_start.append(int(self.table.item(r, c).text()))
                elif c == 2:
                    self.new_end.append(int(self.table.item(r, c).text()))
                else:
                    self.new_weight.append(float(self.table.item(r, c).text()))
        return pd.DataFrame({'Name':self.new_name, 'Start Time':self.new_start, 'End Time': self.new_end, 'Weight': self.new_weight})
    
    def layouts(self):
        ################## Layouts ########################
        self.mainLayout = QVBoxLayout()
        self.topLayout = QHBoxLayout()
        self.middleLayout = QHBoxLayout()
        self.bottomLayout = QHBoxLayout()
        self.middleLayout_Left = QHBoxLayout()
        self.middleLayout_Right = QVBoxLayout()
        ################# Adding Child Layouts #############
        self.middleLayout.addLayout(self.middleLayout_Left, 95)
        self.middleLayout.addLayout(self.middleLayout_Right, 5)
        self.mainLayout.addLayout(self.topLayout)
        self.mainLayout.addLayout(self.middleLayout)
        self.mainLayout.addLayout(self.bottomLayout)
        ################## Adding Widgets ###################
        self.topLayout.addStretch()
        self.topLayout.addWidget(self.title)
        self.topLayout.addStretch()
        self.middleLayout_Left.addWidget(self.table)
        self.middleLayout_Right.addStretch()
        self.middleLayout_Right.addWidget(self.reset_btn)
        self.middleLayout_Right.addWidget(self.add_btn)
        self.middleLayout_Right.addWidget(self.remove_btn)
        self.middleLayout_Right.addStretch()
        self.bottomLayout.addWidget(self.update_this_time, 45)
        self.bottomLayout.addWidget(self.update_as_default, 45)
        self.bottomLayout.addWidget(self.help_btn, 8)
        ################# Setting Main Window Layout ########
        self.setLayout(self.mainLayout)
    
    def styles(self):
        self.title.setStyleSheet(style.single_tele_title())
    
    def connections(self):
        self.help_btn.clicked.connect(self.openHelp)
    
    def openHelp(self):
        self.text = '[Reset]\nreset the table to the default one.\n\n[Add]\nadd a new telescope, you will have to enter: \n ---- name(string)\n ---- start time and end time (non-negative integer)\n ---- weight(float, here we use the squared radius).\n\n[Remove]\nremove the selected row (if more than 2 items in the tale is selected, the row(s) they are on are the selected rows).\n\n[Update This Time]\nuse the edited table for analysis only for this time.\n\n[Update as Default]\nuse this edited table as the default in the future as well.'
        QMessageBox.information(self,'Information', self.text)       
    




        
def main():
    df = pd.read_csv('data/single_tele_default.csv')
    App = QApplication(sys.argv)
    window = Window(df, df)
    sys.exit(App.exec_())

if __name__ == '__main__':
    main()