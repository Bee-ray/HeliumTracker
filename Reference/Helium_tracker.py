import os.path as osp
import numpy as np
from PyQt6.QtWidgets import (QApplication, QComboBox, QDialog, 
                             QGridLayout, QGroupBox, QLabel, 
                             QLineEdit,QPushButton, QStyleFactory,  
                             QTabWidget, QTextEdit,QWidget, QFrame)

from PyQt6.QtTest import QTest
from PyQt6.QtGui import QPalette, QColor
from pyqtgraph.Qt import QtGui, QtCore
import sys
import pyqtgraph as pg
from datetime import datetime
from Reference.Save import Savetxt
from Reference.LevelMeter import HeliumDewar



class LHeLogger(QWidget):  
    measurement=[]
    last=[]
    def __init__(self):
        super.__init__()
        pg.setConfigOptions(antialias=False)
        # pg.setConfigOption('background', 'w') #Sets plot background to white
        # pg.setConfigOption('foreground', 'k') #Sets plot thicks to black
        
        carl=HeliumDewar('Carl', 'ASRL10::INSTR')
        dug=HeliumDewar('Dug','ASRL11::INSTR')
        
        self.instruments=[carl,dug]
        
        """
        Do we need these?
        """
        #Dictionaries for apearence
        
        self.check_value={}
        self.color_value={}
        self.symbol_value={}
        self.label_value={}
        self.edit_value={}

        
        #Apearence parameters
        self.originalPalette = QApplication.palette()
        
        self.font = QtGui.QFont()
        self.font.setFamily('Helvetica')
        self.font.setPointSize(10)
        self.font.setBold(True)
        self.font.setItalic(True)
        
        plot_gb= self.createplot()
        control_gb= self.createControl()
        lv=self.createLevelViewer()
        #Sets position of each group in the GUI
        mainLayout = QGridLayout()
        mainLayout.addWidget(plot_gb, 0, 0, 1, 2)
        mainLayout.addWidget(control_gb, 1, 1, 1, 1)
        mainLayout.addWidget(lv, 1, 0, 1, 1)
        
        mainLayout.setColumnStretch(0,3)
        self.setLayout(mainLayout)

        self.setWindowTitle("Dean Lab Helium Recovery") #Title of the GUI window        
        QApplication.setStyle(QStyleFactory.create('Fusion')) #Style of the GUI
        
    # def createTopMostLeftGroup(self): #Save items
    #     self.TopMostLeftGroup = QGroupBox('SAVE')
    #     GUI.save_GUI(self.TopMostLeftGroup)
        
    def createplot(self): #Plot item
        plot_gb = QGroupBox("Plotting")
        Tab_plot = QTabWidget()
        livetab = QWidget()
        
        Tab_plot.addTab(livetab,'live plot')
        # Tab_plot.addTab(imtab,'2D plots')
        
        data=np.zeros((200,200))
        for i in range(200):
            for j in range(200):
                data[i,j]=np.sin(i*np.pi/100)*np.sin(j*np.pi/200) #Connect real data to this!
        
        self.plot_window = pg.PlotWidget(parent=livetab)
        # self.implot = pg.ImageView(parent=imtab)
        # self.implot.setImage(data)
        
        l1=QGridLayout()
        l1.addWidget(self.plot_window, 0, 0, 1, 1)
        livetab.setLayout(l1)
        
        # l2=QGridLayout()
        # l2.addWidget(self.implot, 0, 0, 1, 1)
        # imtab.setLayout(l2)        
        
        layout = pg.GraphicsLayout()
        # axis = pg.DateAxisItem()
        # self.TopMiddlePlot.setAxisItems({'bottom':axis})
        layout.addPlot()
        self.plot_window.enableAutoRange('x','y', True)
        
        layout = QGridLayout()
        layout.addWidget(Tab_plot, 0, 0, 1, 1)
        layout.setRowStretch(1, 1)
        plot_gb.setLayout(l1)
    
    


        #Creating different plot for all the intruments to plot them on one figure at the time if needed
        self.ax1 = self.plot_window.plot()
        self.ax2 = self.plot_window.plot()
        # self.ax3 = self.TopMiddlePlot.plot()
        # self.ax4 = self.TopMiddlePlot.plot()
        # self.ax5 = self.TopMiddlePlot.plot()
        # self.ax6 = self.TopMiddlePlot.plot()
        # self.ax7 = self.TopMiddlePlot.plot()
        # self.ax8 = self.TopMiddlePlot.plot()
        # self.ax9 = self.TopMiddlePlot.plot()
        # self.ax10 = self.TopMiddlePlot.plot()
        # self.ax11 = self.TopMiddlePlot.plot()
        # self.ax12 = self.TopMiddlePlot.plot()
        # self.ax13 = self.TopMiddlePlot.plot()
        # self.ax14 = self.TopMiddlePlot.plot()
        # self.ax15 = self.TopMiddlePlot.plot()
        self.plotData = {'x':[], 'y':[]}
        self.plotData1 = {'x':[], 'y':[]}
        self.plotData2 = {'x':[], 'y':[]}
        # self.plotData3 = {'x':[], 'y':[]}
        # self.plotData4 = {'x':[], 'y':[]}
        # self.plotData5 = {'x':[], 'y':[]}
        # self.plotData6 = {'x':[], 'y':[]}
        # self.plotData7 = {'x':[], 'y':[]}
        # self.plotData8 = {'x':[], 'y':[]} 
        # self.plotData9 = {'x':[], 'y':[]}
        # self.plotData10 = {'x':[], 'y':[]} 
        # self.plotData11 = {'x':[], 'y':[]} 
        # self.plotData12 = {'x':[], 'y':[]} 
        # self.plotData13 = {'x':[], 'y':[]}
        # self.plotData14 = {'x':[], 'y':[]}                                                                                                
        # self.plotData15 = {'x':[], 'y':[]}
        
        return plot_gb
        
    def createControl(self):
        control_gb = QFrame()
        
        self.StartButton = QPushButton('START')
        self.StartButton.setStyleSheet("background-color: #142c76;")
       
        self.StartButton.clicked.connect(self.plotter)
        
        self.StopButton = QPushButton('STOP')
        self.StopButton.setStyleSheet("background-color: #76142c;" )
        self.StopButton.clicked.connect(self.stopper)
        
        exitButton = QPushButton('CLOSE')
        exitButton.clicked.connect(self.QuitApp)
        
        self.measButton = QPushButton('Set Sample and Measure')
        self.measButton.clicked.connect(self.instruments[1].set_sample)
        
        layout = QGridLayout()
        layout.addWidget(self.StartButton, 0, 0, 1, 1)
        layout.addWidget(self.StopButton, 1, 0, 1, 1)
        layout.addWidget(exitButton, 2, 0, 1, 1)
        layout.addWidget(self.measButton, 3, 0, 1, 1)
        control_gb.setLayout(layout)
        return control_gb
    
    def createLevelViewer(self):
        lv_frame = QFrame()
        labels={}
        self.levels={}
        for i,inst in enumerate(self.instruments):
            labels[i],self.levels[i]=self.levelDisplay(inst.name)
        
        
        layout = QGridLayout()
        
        for i in range(len(self.instruments)):
            layout.addWidget(labels[i], i, 0, 1, 1)
            self.levels[i].setDisabled(True)
            layout.addWidget(self.levels[i], i, 1, 1, 1)
        lv_frame.setLayout(layout)
        return lv_frame
    def clr_plot(self): #Clears plot only, not the data
        self.plotfrom=self.full_data[:,0].size
        
    def plotter(self): #Sets dim of measure and starts timer for live update. Creates folder and file to save

        logdirectory='C:/Users/thecd/Desktop/Helium'
        filename='lHe_log'
        header=['time','carl level (in)','dug level (in)']
        header="\t".join(header)

        userdoc = osp.join(osp.expanduser("~"),logdirectory)
        self.logfile = Savetxt(header,filename,userdoc,'') #no notes
        
        self.measButton.setEnabled(False)
        
        msmttime=datetime.now().isoformat(timespec='minutes')
        msmt=[msmttime]

        
        self.logfile.save_line(msmt)
        
        for i, inst in enumerate(self.instruments):
            lev=inst.measure_level()
            delaytime=self.instruments[0].measurement_interval()
            self.measurement.append([float(lev)])
            self.last.append(float(lev))
            self.levels[i].setText(lev)
            msmt.append(lev)
            
        self.StartButton.setStyleSheet("background-color: #008B45;")
        self.timer = QtCore.QTimer()
        self.timer.timeout.connect(self.updater)
        self.timer.start(int(delaytime*1000))
        
    def pauser(self):
        print('Pause')
        self.timer.stop()
        
    def stopper(self):
        self.StopIsClicked = True
        print('Stop')
        self.timer.stop()
        self.measButton.setEnabled(True)
        # self.full_data=np.array([[]]);self.instr_value=[];
        self.count = 0 #+1 everytime a point is taken
        self.count1 = 0;self.count2 = 0;self.count3 = 0; self.countB = 0; self.countT = 0 #+1 everytime a point in the corresponding loop is taken
        self.loop1 = 0;self.loop2 = 0;self.loop3 = 0; self.loopB = 0; self.loopT = 0; #+1 everytime the corresponding loop has run once
        self.sampleTime=0;
        #Initialization of lists to save data
        self.plotfrom=0
        self.StopIsClicked = False
        self.StartButton.setStyleSheet("background-color: #142c76;")
        
    def updater(self):#Function where plot, and saving of file happens
        msmttime=datetime.now().isoformat(timespec='minutes')
        msmt=[msmttime]
        for i, inst in enumerate(self.instruments):
            lev=inst.measure_level()
            if (np.abs(float(lev)-self.last[i])>.5):
                count=0
                while (count<3 and np.abs(float(lev)-self.last[i])>.5):
                    print(count)
                    inst.force_measure()
                    QTest.qWait(int(10000))
                    lev=inst.measure_level()
                    count+=1
            
            self.levels[i].setText(lev)
            msmt.append(lev)
            self.measurement[i].append(float(lev))
            self.last[i]=float(lev)
        self.logfile.save_line(msmt)
        
        self.plot_window.clear()
        xdata=np.linspace(0,len(self.measurement[0]),num=len(self.measurement[0]))
        self.plot_window.plot(xdata,np.array(self.measurement[0]),symbol='o')
        self.plot_window.plot(xdata,np.array(self.measurement[1]),symbol='o')

    def QuitApp(self):
        #B_control.close()
        self.close()
        
    def levelDisplay(self,instr_name):
        name=QLabel(instr_name)
        level= QLineEdit()
        
        return name,level


#Lines to call the app and run it      
app = QApplication(sys.argv)
palette = QPalette()
palette.setColor(QPalette.Window, QColor(53, 53, 53))
palette.setColor(QPalette.WindowText, QtCore.Qt.white)
palette.setColor(QPalette.Base, QColor(25, 25, 25))
palette.setColor(QPalette.AlternateBase, QColor(53, 53, 53))
palette.setColor(QPalette.ToolTipBase, QtCore.Qt.black)
palette.setColor(QPalette.ToolTipText, QtCore.Qt.white)
palette.setColor(QPalette.Text, QtCore.Qt.white)
palette.setColor(QPalette.Button, QColor(53, 53, 53))
palette.setColor(QPalette.ButtonText, QtCore.Qt.white)
palette.setColor(QPalette.BrightText, QtCore.Qt.red)
palette.setColor(QPalette.Link, QColor(42, 130, 218))
palette.setColor(QPalette.Highlight, QColor(42, 130, 218))
palette.setColor(QPalette.HighlightedText, QtCore.Qt.black)
app.setPalette(palette)
gallery = LHeLogger()
gallery.show()
app.exec_()