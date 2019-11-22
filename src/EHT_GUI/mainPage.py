import sys
from PyQt5.QtWidgets import *
from PyQt5.QtGui import QPixmap, QIcon, QFont
from PyQt5.QtCore import Qt
import pandas as pd
import numpy as np
import Adv_singleTele, Adv_penalty, Adv_length, modeling, style


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setGeometry(220, 150, 600, 350) # Location(X,Y) and Size(X,Y) of the Window
        self.penaltyLevelValue = 0
        self.setFixedSize(600, 350)
        
        self.singleDefault = pd.read_csv('data/single_tele_default.csv')
        self.singleCurrent = self.singleDefault.copy()
        self.display = self.singleCurrent.copy()
        self.lengthDefault = pd.read_csv('data/baseline_length_default.csv')

        self.UI()
        self.setWindowTitle('Optimal Real-Time Scheduling')
        self.show() 

    def UI(self):
        self.mainDesign()
        self.layouts()
        self.createMenu()
        self.connections()
        self.styles()

    def createMenu(self):
        self.menubar = self.menuBar()
        self.menubar.setNativeMenuBar(False) # For MacOS
        self.advanced = self.menubar.addMenu("Advanced")
        self.helpMenu = self.menubar.addMenu("Help")
        self.exitMenu = self.menubar.addMenu("Exit")


        self.single_tele = QAction('Single Telescope Info')
        self.advanced.addAction(self.single_tele)
        self.length_tele = QAction('Baseline Length')
        self.advanced.addAction(self.length_tele)
        self.penalty_level= QAction('Penalty Level')
        self.advanced.addAction(self.penalty_level)
        self.reward_function= QAction('Reward Function')
        self.advanced.addAction(self.reward_function)
        self.exit_function = QAction('Exit')
        self.exitMenu.addAction(self.exit_function)

        self.default_value = QAction('Default Values')
        self.helpMenu.addAction(self.default_value)
        self.more_info = QAction('More Information')
        self.helpMenu.addAction(self.more_info)


    def mainDesign(self):
        ### Top ###
        self.eht_image = QLabel(self)
        self.pixmap = QPixmap('images/eht.png')
        self.sizedPixmap = self.pixmap.scaled(600,1024, Qt.KeepAspectRatio)
        self.eht_image.setPixmap(self.sizedPixmap)
        ### Middle - Left ###
        self.data_txt = QLabel('Data Path: ')
        self.data_btn = QPushButton('  Open File   ', self)
        self.data_btn.setIcon(QIcon('icons/folder.png'))
        self.data_btn.clicked.connect(self.openFile)
        self.start_txt = QLabel('Start Date: ')
        self.start_input = QLineEdit()
        self.start_input.setPlaceholderText(' YYYY-MM-DD')
        self.end_txt = QLabel('End Date: ')
        self.end_input = QLineEdit()
        self.end_input.setPlaceholderText(' YYYY-MM-DD')
        self.days_txt = QLabel('Days to Tigger: ')
        self.days_input = QLineEdit()
        self.days_input.setPlaceholderText(' Positive Integer')
        self.middleLeft_keyList = [self.data_txt, self.start_txt, self.end_txt, self.days_txt]
        self.middleLeft_valueList = [self.data_btn, self.start_input, self.end_input, self.days_input]
        ### Middle - Right ###
        self.right_title = QLabel('          Advanced Settings')
        self.single_tele_txt = QLabel('Single Telescope Info: ')
        self.single_tele_status = QLabel('Default  ')
        self.length_tele_txt = QLabel('Baseline Length: ')
        self.length_tele_status = QLabel('Default  ')
        self.penalty_level_txt = QLabel('Penalty Level: ')
        self.penalty_level_status = QLabel('Default  ')
        self.reward_func_txt = QLabel('Reward Function: ')
        self.reward_func_status = QLabel('Default  ')
        self.middleRight_keyList = [self.single_tele_txt, self.length_tele_txt, self.penalty_level_txt, self.reward_func_txt]
        self.middleRight_valueList  = [self.single_tele_status, self.length_tele_status, self.penalty_level_status, self.reward_func_status]
        ### Bottom ###
        self.run_btn = QPushButton('RUN', self)       
        

    def layouts(self):
        self.wid = QWidget(self)
        self.setCentralWidget(self.wid)
        ################## Layouts ########################
        self.mainLayout = QVBoxLayout()
        self.topLayout = QHBoxLayout()
        self.middleLayout = QHBoxLayout()
        self.bottomLayout = QHBoxLayout()
        self.middleLayout_Left = QFormLayout()
        self.middleLayout_Right = QVBoxLayout()
        self.middleLayout_RightTop = QHBoxLayout()
        self.middleLayout_RightBottom = QFormLayout()
        ################# Adding Child Layouts #############
        self.middleLayout_Right.addLayout(self.middleLayout_RightTop)
        self.middleLayout_Right.addLayout(self.middleLayout_RightBottom)
        self.middleLayout.addStretch()
        self.middleLayout.addLayout(self.middleLayout_Left, 45)
        self.middleLayout.addLayout(self.middleLayout_Right, 55)
        self.middleLayout.addStretch()
        self.mainLayout.addLayout(self.topLayout)
        self.mainLayout.addLayout(self.middleLayout)
        self.mainLayout.addLayout(self.bottomLayout)
        ################## Adding Widgets ###################
        for i in range(len(self.middleLeft_keyList)):
            self.middleLayout_Left.addRow(self.middleLeft_keyList[i], self.middleLeft_valueList[i])
        for j in range(len(self.middleRight_keyList)):
            self.middleLayout_RightBottom.addRow(self.middleRight_keyList[j], self.middleRight_valueList[j])
        self.middleLayout_RightTop.addStretch()
        self.middleLayout_RightTop.addWidget(self.right_title)
        self.middleLayout_RightTop.addStretch()
        self.topLayout.addWidget(self.eht_image)
        self.bottomLayout.addWidget(self.run_btn)
        ################# Setting Main Window Layout ########
        self.wid.setLayout(self.mainLayout)  

    def styles(self):
        self.run_btn.setStyleSheet(style.runBtn())      

    def openFile(self):
        url = QFileDialog.getExistingDirectory(self, 'Open a file')
        if len(url) != 0:
            self.data_btn.setText('   Re-Open   ')
    
    def connections(self):
        self.exit_function.triggered.connect(self.exitFunc)
        self.single_tele.triggered.connect(self.openSingleTele)
        self.length_tele.triggered.connect(self.openLengthTele)
        self.penalty_level.triggered.connect(self.openPenalty)
        self.run_btn.clicked.connect(self.addRun)
    
    def exitFunc(self):
        exitMbox = QMessageBox.question(self, 'Warning', 'Are you sure to exit? \nAll temporary results and updates will be lost.', QMessageBox.Yes|QMessageBox.No, QMessageBox.No)
        if exitMbox == QMessageBox.Yes:
            sys.exit()

    ############### Single Tele Connections #########
    def openSingleTele(self):
        self.run_singleTele = Adv_singleTele.Window(self.singleCurrent, self.singleDefault)
        self.run_singleTele.update_this_time.clicked.connect(self.updateSingleTeleThisTime)
        self.run_singleTele.update_as_default.clicked.connect(self.updateSingleTeleDefault)
        self.run_singleTele.reset_btn.clicked.connect(self.resetValue)
        self.run_singleTele.add_btn.clicked.connect(self.addRow)
        self.run_singleTele.remove_btn.clicked.connect(self.removeRow)
      
    def resetValue(self):
        self.run_singleTele.setTable(self.singleDefault)
        self.display = self.singleDefault
    
    def addRow(self):
        to_add = [' ',' ',' ',' ',' ']
        self.display = pd.DataFrame(dict(zip(self.display.columns, to_add)), index = [-1]).append(self.display)
        self.run_singleTele.setTable(self.display)
    
    def removeRow(self):
        self.run_singleTele.selected = self.run_singleTele.table.selectedItems()
        if len(self.run_singleTele.selected) > 1:
            self.delete_row = []
            for item in self.run_singleTele.selected:
                if item.row() not in self.delete_row:
                    self.delete_row.append(item.row())
            
            self.display = self.display.drop(list(np.array(self.display.index)[self.delete_row]))
            self.run_singleTele.setTable(self.display)     
        else:
            QMessageBox.information(self, 'Information', 'Please select at least one row to remove.')
   

    def updateSingleTeleThisTime(self):
        self.singleCurrent = self.run_singleTele.writeDf()
        self.single_tele_status.setText('Updated')
        self.single_tele_status.setStyleSheet(style.singleTeleUpdate())
        self.run_singleTele.close()

    def updateSingleTeleDefault(self):
        self.singleCurrent = self.run_singleTele.writeDf()
        self.singleDefault = self.run_singleTele.writeDf()
        self.singleDefault.to_csv('data/single_tele_default.csv', index = False)

        self.single_tele_status.setText('Updated')
        self.single_tele_status.setStyleSheet(style.singleTeleUpdate())
        self.run_singleTele.close()


    ############### Baseline Length Connections #########
    def openLengthTele(self):
        self.run_lengthTele = Adv_length.Window(self.lengthDefault)
        self.run_lengthTele.update_btn.clicked.connect(self.updateBaselineLength)
    
    def updateBaselineLength(self):
        self.lengthDefault = self.run_lengthTele.writeDf()
        self.lengthDefault.to_csv('data/baseline_length_default.csv', index = False)

        self.length_tele_status.setText('Updated')
        self.length_tele_status.setStyleSheet(style.singleTeleUpdate())
        self.run_lengthTele.close()

    ############### Penalty Term Connections #########
    def openPenalty(self):
        self.run_penaltyLevel = Adv_penalty.Window()
        self.run_penaltyLevel.update_btn.clicked.connect(self.updatePenalty)
    
    def updatePenalty(self):
        if len(self.run_penaltyLevel.window_penalty_txt.text()) == 0:
            QMessageBox.information(self,'Warning', 'Please enter a number.')  
        else:
            self.penaltyLevelValue = self.run_penaltyLevel.window_penalty_txt.text()
            self.penalty_level_status.setText(str(self.penaltyLevelValue))
            self.penalty_level_status.setStyleSheet(style.singleTeleUpdate())
            self.run_penaltyLevel.close()
    

        

    ############### Run Model Connections ###########
    def addRun(self):
        self.run_Model = modeling.Window()

        
def main():
    App = QApplication(sys.argv)
    window = MainWindow()
    sys.exit(App.exec_())

if __name__ == '__main__':
    main()