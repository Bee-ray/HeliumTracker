
from PyQt6.QtWidgets import (QApplication, 
                             QStyleFactory,
                             QMainWindow,
                             QTabWidget)
from PyQt6.QtGui import QPalette, QColor
import json
from LHePlot import LHePlot
from LHeRecord import LHeRecorder

# Read Configs from the config file
with open('Config\\Config.dat') as f:
    config = json.load(f)
# Config format: a dictionary that contains:
    # instruments: a dictionary that contains the name of the instruemnt and its serial address.
    # symbols： the symbols array used to plot when recording He level, corresponding to each instruemtn.
    # colors: the color array used to record&fit He level corresponding to each instrument. The size should be no smaller than the number of instruments.


class LHeTracker(QMainWindow):
    # LHeTracker class inherited from QMainWindow. It is the Main window of the LHe Tracker application
    def __init__(self, size=(1280,960)):
        super().__init__()
        self.size = size
        self.setWindowTitle('Dean Lab Helium Tracker') # Set the title
        self.setFixedSize(size[0],size[1]) # Size is fixed as there is no need to scale it.
        
        # Add functional tabs to the window
        self.tabs = QTabWidget()
        self.live_tab = LHeRecorder(config) # The real-time He recording tab.
        self.fitting_tab = LHePlot(config) # The tab that reads the previous log and fit the rate.
        self.tabs.addTab(self.live_tab,'Live')
        self.tabs.addTab(self.fitting_tab,'Fitting')
        self.setCentralWidget(self.tabs)
        
app = QApplication([])
QApplication.setStyle(QStyleFactory.create('Fusion')) # Style of the GUI

# Some GUI color settings. Considering putting all these configs in a file.
palette = QPalette()
palette.setColor(QPalette.ColorRole.Window, QColor(53, 53, 53))
palette.setColor(QPalette.ColorRole.WindowText, QColor(255,255,255))
palette.setColor(QPalette.ColorRole.Base, QColor(25, 25, 25))
palette.setColor(QPalette.ColorRole.AlternateBase, QColor(53, 53, 53))
palette.setColor(QPalette.ColorRole.ToolTipBase, QColor(0,0,0))
palette.setColor(QPalette.ColorRole.ToolTipText, QColor(255,255,255))
palette.setColor(QPalette.ColorRole.Text, QColor(255,255,255))
palette.setColor(QPalette.ColorRole.Button, QColor(53, 53, 53))
palette.setColor(QPalette.ColorRole.ButtonText, QColor(255,255,255))
palette.setColor(QPalette.ColorRole.BrightText, QColor(255,0,0))
palette.setColor(QPalette.ColorRole.Link, QColor(42, 130, 218))
palette.setColor(QPalette.ColorRole.Highlight, QColor(42, 130, 218))
palette.setColor(QPalette.ColorRole.HighlightedText, QColor(0,0,0))
app.setPalette(palette)

# Create the window and run the app
He = LHeTracker()
He.show()
app.exec()