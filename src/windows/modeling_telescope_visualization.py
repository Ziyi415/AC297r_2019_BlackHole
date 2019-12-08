import sys
from PyQt5.QtWidgets import *

from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar
import matplotlib.pyplot as plt
import numpy as np

class Window(QDialog):
    def __init__(self, df,parent=None):
        super(Window, self).__init__(parent)

        # a figure instance to plot on
        self.figure = plt.figure(tight_layout=True)

        # this is the Canvas Widget that displays the `figure`
        # it takes the `figure` instance as a parameter to __init__
        self.canvas = FigureCanvas(self.figure)

        # this is the Navigation widget
        # it takes the Canvas widget and a parent
        self.toolbar = NavigationToolbar(self.canvas, self)

        # set the layout
        layout = QVBoxLayout()
        layout.addWidget(self.toolbar)
        layout.addWidget(self.canvas)
        self.setLayout(layout)

        self.plot(df)

    def plot(self, df):
        ''' plot some random stuff '''
        plt.pcolor(1/df)
        plt.yticks(np.arange(0.5, len(df.index), 1), df.index)
        plt.xticks(np.arange(0.5, len(df.columns), 1), df.columns)

        # refresh canvas
        self.canvas.draw()

if __name__ == '__main__':
    import pandas as pd
    app = QApplication(sys.argv)
    df = pd.read_csv('data/tau_df.csv', index_col = 0)

    main = Window(df)
    main.show()

    sys.exit(app.exec_())