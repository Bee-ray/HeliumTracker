import os.path as osp
from PyQt6.QtWidgets import (QWidget,
                             QPushButton, 
                             QFileDialog, 
                             QLabel, 
                             QVBoxLayout, 
                             QHBoxLayout, 
                             QSlider, 
                             QComboBox,
                             QLineEdit)

from PyQt6.QtCore import Qt
import pyqtgraph as pg
import numpy as np
import lmfit.models as models
from LHeDewar import LHeDewar

class LHePlot(QWidget):
    '''
    A Qwidget that can be directly implanted into another Qwidget/Qwindow
    Read a log that was created by LHeRecord, plot the data, calculate the volume regarding the level, and selectively fit the slope
    '''
    def __init__(self, config):
        # need to the config to set the plotting style.
        super().__init__()
        self.s = config['symbols']
        self.c = config['colors']

        # call the funtions that create Qwidgets
        self.createOpenFileButton()
        self.createGraph()
        self.createSlider()
        self.createComboBox()
        self.createSlopeBox()
        self.createFitButton()

        # set the layout of all widgets
        
        # the top horizontal box that contains the open button and the filename lineedit box.
        hbox1 = QHBoxLayout()
        hbox1.addWidget(self.button_openfile)
        hbox1.addWidget(self.lineedit_filename,1)
        
        # the bottom horizontal box that contains:
            # the combo box that select the instruments
            # the sliders that decides the range to do linear fit
            # the button that activate the fitting
            # the textbox that shows the calculated liquefying rate
        hbox2 = QHBoxLayout()
        hbox2.addWidget(QLabel('Instrument:'))
        hbox2.addWidget(self.combo_box)
        hbox2.addStretch(1)
        hbox2.addWidget(QLabel("From"))
        hbox2.addWidget(self.slider_start)
        hbox2.addWidget(self.slider_start_value)
        hbox2.addWidget(QLabel('   to'))
        hbox2.addWidget(self.slider_end)
        hbox2.addWidget(self.slider_end_value)
        hbox2.addWidget(self.button_fit)
        hbox2.addStretch(1)
        hbox2.addWidget(QLabel('Rate:'))
        hbox2.addWidget(self.lineedit_slope)
        hbox2.addWidget(QLabel('L/Day'))

        # the vertal box that contains the two horizontal box at top and bottom and the graph in between.
        vbox = QVBoxLayout()
        vbox.addLayout(hbox1)
        vbox.addWidget(self.graph)
        vbox.addLayout(hbox2)
        
        self.setLayout(vbox)


    def createGraph(self):
        # Create the graph
        self.graph = pg.plot()
        self.graph.setLabel(axis = 'left', text = 'Volume(L)')
        self.graph.setLabel(axis = 'bottom', text = 'Time(h)')
        self.line = None # the fitting line
        self.data = [] # 2d array that stores the volume data of each instrument
        self.scatter = [] # array that stores the scatter plot objects, which is esentially line object with blank pen.


    def createOpenFileButton(self):
        # Create the open file button and the filename lineedit box
        self.lineedit_filename = QLineEdit()
        self.lineedit_filename.setReadOnly(True)
        self.button_openfile = QPushButton('OPEN')
        self.button_openfile.clicked.connect(self.openFile)
        

    def createSlopeBox(self):
        # Create the lineedit box that shows the fitting slope
        self.lineedit_slope = QLineEdit()
        self.lineedit_slope.setReadOnly(True)
        

    def createSlider(self):
        '''
        Create the two sliders that decide the range of fitting.
        Since QSlider has only integer value set, it is value/2 that represents the actual time in hour, as the level is usually recorded every 30 mins. 
        '''
        def selecFitRange():
            
            self.slider_end.setMinimum(self.slider_start.value()+1) # When slider_start changes we need to correspondingly change the minimum value of slider_end
            self.slider_start_value.setText(str(self.slider_start.value()/2.))
            self.slider_end_value.setText(str(self.slider_end.value()/2.))
        
        self.slider_start = QSlider(Qt.Orientation.Horizontal)
        self.slider_start.setMinimum(0)
        self.slider_start.setMaximum(0)
        self.slider_start.valueChanged.connect(selecFitRange)
        self.slider_start.setFixedWidth(300)
        self.slider_end = QSlider(Qt.Orientation.Horizontal)
        self.slider_end.setMinimum(1)
        self.slider_end.setMaximum(1)
        self.slider_end.valueChanged.connect(selecFitRange)
        self.slider_end.setFixedWidth(300)
        self.slider_start_value = QLabel(str(self.slider_start.value()/2.))
        self.slider_end_value = QLabel(str(self.slider_end.value()/2.))


    def createComboBox(self):
        # create the combo box that choose which instrument to fit
        self.combo_box = QComboBox()
        self.combo_box.setCurrentIndex(0)
        self.objectChanged = True


    def createFitButton(self):
        # Create the button that activate the fit funciton
        self.button_fit = QPushButton('FIT')
        self.button_fit.clicked.connect(self.plotLinearFit)


    def openFile(self):
        # Called when clicking the openfile button
        self.old = False

        logdirectory='Desktop\\HeliumLogs'
        default_directory = osp.join(osp.expanduser("~"),logdirectory)
        self.filename= QFileDialog.getOpenFileName(parent = self, directory = default_directory, caption = 'Open File')[0]
        
        self.lineedit_filename.setText(self.filename)
        self.combo_box.clear()

        with open(self.filename) as f:
            line = f.readline()
            if line == '\n':
                # check if the log file is created by Jordan's old logging app
                line = f.readline()
                self.old = True 
            headers = line.split('\t') # read the first line as the header of the numpy file
            self.instruments = []
            for i in range(1,len(headers)):
                # add the names got from the file to the combo box
                name = headers[i].split(' ')[0].capitalize()
                self.instruments.append(LHeDewar(name))
                self.combo_box.addItem(name)
                
        self.plotHeliumData()


    def plotHeliumData(self):
        # clear all the attributes and the graph
        names = ['Time']
        self.graph.clear()
        self.line = None
        self.data = []
        self.scatter = []

        for i in range(len(self.instruments)):
            names.append(self.instruments[i].getName())

        # raw data is the numpy that contains the level information, which will be converted to volume later
        if self.old:
            rawdata = np.genfromtxt(self.filename, skip_header = 3,names = names, dtype = ['datetime64[s]'] + len(self.instruments)*[np.float64])
        else:
            rawdata = np.genfromtxt(self.filename, skip_header = 1,names = names, dtype = ['datetime64[s]'] + len(self.instruments)*[np.float64])
        
        self.timer = (rawdata['Time'] - rawdata['Time'][0]).astype(np.float64)/3600.

        # According to the range of the data, set the minimum and maximum of the range
        self.slider_end.setMinimum(1)
        self.slider_end.setMaximum(round(self.timer[-1]*2))
        self.slider_end.setValue(round(self.timer[-1]*2))
        self.slider_start.setMaximum(round(self.timer[-1]*2)-1)

        self.legend = self.graph.addLegend((1,1)) # add legend at top left corner

        for i in range(len(self.instruments)):
            # get an array of volume data calculated from the raw data from the file
            self.data.append(self.instruments[i].levelToVolume(rawdata[self.instruments[i].getName()]))
            # plot the converted volume data
            self.scatter.append(self.graph.plot(self.timer, self.data[i], name = self.instruments[i].getName(),symbol = self.s[i], symbolpen = None, pen = None, symbolSize = min(8,1200/len(self.timer))))
            # set the color according to the colors array in the config file
            self.scatter[-1].setSymbolBrush(self.c[i])


    def plotLinearFit(self):
        # find the start and end index of the fitting dataset.
        start = np.abs(self.timer - self.slider_start.value()/2.0).argmin()
        end = np.abs(self.timer - self.slider_end.value()/2.0).argmin()
        if start == end:
            return

        # The instrument to fit        
        i = self.combo_box.currentIndex()
        current_instrument = self.instruments[i].getName()

        if end == 0:
            end = len(self.data[i]) - 1

        # linefit model
        linefit = models.LinearModel()
        params = linefit.guess(self.data[i][start:end+1], self.timer[start:end+1])
        linefit_result = linefit.fit(self.data[i][start:end+1], params, x=self.timer[start:end+1])

        if not self.line:
            # draw the line fit line
            self.line = self.graph.plot(self.timer[start:end+1], linefit_result.best_fit, name = current_instrument +'_Fit',pen = pg.mkPen(color = self.c[i],width = 4))
        else:
            # if a line already exists, update it
            self.line.setData(self.timer[start:end+1], linefit_result.best_fit)
            if self.objectChanged == True:
                self.line.setPen(self.c[i],width = 4)
                self.legend.removeItem(self.line)
                self.legend.addItem(self.line, current_instrument+"_Fit")

        rate = linefit_result.params['slope'].value*24
        # calculate and show the rate
        self.lineedit_slope.setText(str('%.2f' % rate))