import pyvisa #for intstrument communication
import lmfit.models as models
import numpy as np

rm = pyvisa.ResourceManager()
resources = rm.list_resources()

class LHeDewar:
    
    #might be worth making the level meter instrument a class variable here.
    #Plus add serial comm commands

    def __init__(self, name, resource = None):
        if resource in resources:
            self.lm = rm.open_resource(resource)
        else:
            self.lm = None
        self.name = name
        calib = np.genfromtxt('Config\\Calibration_'+name+'.dat',skip_header = 1)
        self._spline = models.SplineModel(perfix = "spline_" + self.name, xknots = calib[:,0])
        self._params = self._spline.guess(calib[:,1],calib[:,0])
        self._sp_out = self._spline.fit(calib[:,1],self._params,x=calib[:,0])

    def getName(self):
        return self.name

    def levelToVolume(self,levels):
        return self._sp_out.eval(self._params, x = levels)

    def measureLevel(self):
        if self.lm:
            try:
                self.lm.query('MEAS?')
                lev=self.lm.read().split(" ")[0]
            except pyvisa.errors.VisaIOError:
                lev = '-1001'
            return lev
        else:
            return '-2001'

    def forceMeasure(self):
        if self.lm:
            try:
                self.lm.query('MEAS')
            except:
                pass
    
    def setSample(self):
        if self.lm:
            try:
                self.lm.query('MODE S')
                self.lm.query('MEAS')
            except:
                pass
        
    def stb(self):
        if self.lm:
            try:
                self.lm.query('*STB?')
                return self.lm.read()
            except pyvisa.errors.VisaIOError:
                return '-1001'
        else:
            return '-2001'
    
    def measurementInterval(self):
        if self.lm:
            try:
                self.lm.query('INTVL?')
                measinterval=self.lm.read().split(':')
                return int(measinterval[0])*3600+int(measinterval[1])*60+int(measinterval[2]) #measurement interval in seconds

            except pyvisa.errors.VisaIOError:
                return 0
        else:
            return 0
    