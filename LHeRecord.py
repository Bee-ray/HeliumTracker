import os.path as osp
import numpy as np
from PyQt6.QtWidgets import (QGridLayout, 
                             QHBoxLayout,
                             QVBoxLayout,
                             QLabel, 
                             QLineEdit,
                             QPushButton,
                             QWidget)

from PyQt6.QtTest import QTest
from PyQt6.QtCore import QTimer
import pyqtgraph as pg
from datetime import datetime
from LHeDewar import LHeDewar
from Save import SaveDat

class LHeRecorder(QWidget):
    def __init__(self, config):
        super().__init__()
        self.s = config['symbols']
        self.c = config['colors']
        self.devices = config['instruments']
        self.instruments = []
        for name, resource in self.devices.items():
            self.instruments.append(LHeDewar(name,resource))

        self.createPlot()
        self.createControlButtons()
        self.createLevelViewers()
        self.createPathViewer()
        self.createTimer()

        self.top = QHBoxLayout()
        self.top.addWidget(self.label_path)
        self.top.addWidget(self.lineedit_path,1)    
        
        self.grid = QGridLayout()
        for i in range(len(self.instruments)):
            hbox = QHBoxLayout()
            label = QLabel(self.instruments[i].getName())
            label.setFixedWidth(50)
            hbox.addWidget(label)
            hbox.addWidget(self.viewers[i])
            hbox.addWidget(QLabel('in'))
            hbox.addStretch(1)
            self.grid.addLayout(hbox, i%3 , i//3)

        self.grid.addWidget(self.button_start,0,5)
        self.grid.addWidget(self.button_stop,1,5)
        self.grid.addWidget(self.button_sample,2,5)

        self.vbox = QVBoxLayout()
        self.vbox.addLayout(self.top)
        self.vbox.addWidget(self.graph)
        self.vbox.addLayout(self.grid)
        self.setLayout(self.vbox)
        

    def createPlot(self):
        self.graph = pg.plot()
        self.graph.setLabel(axis = 'left', text = 'Level(in)')
        self.graph.setLabel(axis = 'bottom', text = 'Time(h)')
        self.last = []
        self.data = []
        self.scatter = []


    def createPathViewer(self):
        self.lineedit_path = QLineEdit()
        self.lineedit_path.setReadOnly(True)
        self.label_path = QLabel('Save Path:')


    def createControlButtons(self):
        self.button_start = QPushButton('START')
        self.button_start.setStyleSheet("background-color: #11B93E")
        self.button_start.clicked.connect(self.start)
        
        self.button_stop = QPushButton('STOP')
        self.button_stop.setEnabled(False)
        self.button_stop.setStyleSheet("background-color: #838080" )
        self.button_stop.clicked.connect(self.stop)

        self.button_sample = QPushButton('SAMPLE')
        self.button_sample.clicked.connect(self.sample)
        self.button_sample.setStyleSheet("background-color: #4D579A" )

    def createLevelViewers(self):
        self.viewers = []
        self.labels = []
        for i in range(len(self.instruments)):
            self.labels.append(QLabel(self.instruments[i].getName()))
            self.viewers.append(QLineEdit())
            self.viewers[-1].setReadOnly(True)
    

    def createTimer(self):
        self.timer = QTimer()
        self.timer.timeout.connect(self.update)


    def start(self):
        self.button_start.setEnabled(False)
        self.button_start.setStyleSheet("background-color: #838080")

        logdirectory='Desktop\\HeliumLogs'
        userdoc = osp.join(osp.expanduser("~"),logdirectory)
        filename='LHe_log'
        header=['Time']
        
        for i in range(len(self.instruments)):
            header.append(self.instruments[i].getName() + ' level(in)')

        self.logfile = SaveDat(userdoc, filename, header = header) #no notes
        self.lineedit_path.setText(self.logfile.filename)
        
        delaytime = 10
        for inst in self.instruments:
            delaytime = max(delaytime,inst.measurementInterval())
        
        for inst in self.instruments:
            inst.setSample()
            QTest.qWait(int(1000))
        QTest.qWait(int(10000))

        self.last = []
        self.data = []
        self.scatter = []
        self.timediff = [0.]

        self.legend = self.graph.addLegend((1,1))

        self.start_time = datetime.now()
        measurement = [self.start_time.isoformat(timespec='minutes')]

        for i, inst in enumerate(self.instruments):
            lev=inst.measureLevel()
            self.last.append(float(lev))
            self.data.append([float(lev)])
            self.viewers[i].setText(lev)
            measurement.append(lev)
            self.scatter.append(self.graph.plot(self.timediff, self.data[i], name = self.instruments[i].getName(), symbol = self.s[i], symbolpen = None, pen = None, symbolSize = 8))
            self.scatter[-1].setSymbolBrush(self.c[i])

        self.logfile.saveLine(measurement)
        self.timer.start(int(delaytime*1000))
        
        self.button_stop.setEnabled(True)
        self.button_stop.setStyleSheet("background-color: #76142c")

          
    def update(self):
        measurement_time=datetime.now()
        measurement=[measurement_time.isoformat(timespec='minutes')]
        self.timediff.append((measurement_time - self.start_time).total_seconds()/3600.)
        
        for i, inst in enumerate(self.instruments):
            lev=inst.measureLevel()
            if (np.abs(float(lev)-self.last[i])>.5):
                count=0
                while (count<3 and np.abs(float(lev)-self.last[i])>.5):
                    inst.forceMeasure()
                    QTest.qWait(int(10000))
                    lev=inst.measureLevel()
                    count+=1
            self.viewers[i].setText(lev)
            measurement.append(lev)
            self.data[i].append(float(lev))
            self.last[i]=float(lev)
            self.scatter[i].setData(self.timediff, self.data[i])

        self.logfile.saveLine(measurement)

            
    def stop(self):
        self.timer.stop()
        self.graph.clear()
        for i in range(len(self.viewers)):
            self.viewers[i].clear()

        self.button_start.setEnabled(True)
        self.button_start.setStyleSheet("background-color: #11B93E")
        self.button_stop.setEnabled(False)
        self.button_stop.setStyleSheet("background-color: #838080" )

    def sample(self):
        start_enabled = False
        end_enabled = False
        if self.button_start.isEnabled():
            start_enabled = True
        if self.button_stop.isEnabled():
            end_enabled = True
        self.button_start.setEnabled(False)
        self.button_start.setStyleSheet("background-color: #838080")
        self.button_stop.setEnabled(False)
        self.button_stop.setStyleSheet("background-color: #838080" )
        self.button_sample.setEnabled(False)
        self.button_sample.setText('WAIT')
        self.button_stop.setStyleSheet("background-color: #838080" )

        for inst in self.instruments:
            inst.setSample()
            QTest.qWait(int(1000))
        QTest.qWait(int(10000))

        if start_enabled:
            self.button_start.setEnabled(True)
            self.button_start.setStyleSheet("background-color: #11B93E")
        if end_enabled:
            self.button_stop.setEnabled(True)
            self.button_stop.setStyleSheet("background-color: #76142c" )
        self.button_sample.setEnabled(True)
        self.button_sample.setText('SAMPLE')
        self.button_sample.setStyleSheet("background-color: #4D579A" )