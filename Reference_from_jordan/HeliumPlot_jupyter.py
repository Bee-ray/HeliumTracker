import numpy as np
import matplotlib.pyplot as plt
import matplotlib.colors as colors
import matplotlib.cbook as cbook
import matplotlib
import scipy.constants as sc
import lmfit.models as models


class HeliumPlot:
    calib = np.genfromtxt('Calibration.txt',delimiter = ',')
    spline = models.SplineModel(perfix = "spline_",xknots = calib[:,0])
    params = spline.guess(calib[:,1],calib[:,0])
    sp_out = spline.fit(calib[:,1],params,x=calib[:,0])

    def __init__(self,filename, delimiter = '\t'):
        self.filename = filename
        self.delimiter = delimiter
        rawdata = np.genfromtxt(self.filename+'.dat', delimiter = self.delimiter, skip_header = 3,names = ['Time','Carl','Dug'], dtype = ['datetime64[s]',np.float64,np.float64])
        self.timer = (rawdata['Time'] - rawdata['Time'][0]).astype(np.float64)/3600.

        self.carl = HeliumPlot.spline.eval(HeliumPlot.params, x = rawdata['Carl'])
        self.dug = HeliumPlot.spline.eval(HeliumPlot.params, x = rawdata['Dug'])

    def plot(self, carlfitrange=None, dugfitrange=None):
        
        self.fig,self.ax = plt.subplots(1,1,figsize = (8,8))
        self.ax.set_title('Helium Log')
        self.ax.set_xlabel('Time(h)')
        self.ax.set_ylabel('Volumn(L)')
        self.scatter_carl = self.ax.scatter(self.timer,self.carl,s = 0.5)
        self.scatter_dug = self.ax.scatter(self.timer,self.dug,s = 0.5)
        
        cinds = dinds = 0
        cinde = dinde = self.timer.shape[0]
        if carlfitrange:
            cinds = np.abs(self.timer - carlfitrange[0]).argmin()
            cinde = np.abs(self.timer - carlfitrange[1]).argmin()
        if dugfitrange:
            dinds = np.abs(self.timer - dugfitrange[0]).argmin()
            dinde = np.abs(self.timer - dugfitrange[1]).argmin()
        
        linefit_carl = models.LinearModel(perfix = "line_carl_")
        params_carl = linefit_carl.guess(self.carl[cinds:cinde+1], self.timer[cinds:cinde+1])
        carlfit = linefit_carl.fit(self.carl[cind s:cinde+1], params_carl, x=self.timer[cinds:cinde+1])
        
        linefit_dug = models.LinearModel(perfix = "line_dug_")
        params_dug = linefit_dug.guess(self.dug[dinds:dinde+1], self.timer[dinds:dinde+1])
        dugfit = linefit_dug.fit(self.dug[dinds:dinde+1],params_dug, x = self.timer[dinds:dinde+1])
        carlrate = carlfit.params['slope'].value*24
        dugrate = dugfit.params['slope'].value*24
        
        self.line_carl = self.ax.plot(self.timer[cinds:cinde+1],carlfit.best_fit, label = 'Carl '+str('%.1f' % carlrate)+" L/day")
        self.line_dug = self.ax.plot(self.timer[dinds:dinde+1],dugfit.best_fit, label = 'Dug '+str('%.1f' % dugrate)+" L/day")
        self.ax.legend()
        
        