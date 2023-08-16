# -*- coding: utf-8 -*-
"""
Created on Mon Aug  8 12:34:55 2022

@author: thecd
"""
import pyvisa #for intstrument communication
import lmfit.models as models
import numpy as np

rm = pyvisa.ResourceManager()

class HeliumDewar:
    
    #might be worth making the level meter instrument a class variable here.
    #Plus add serial comm commands

    def __init__(self, name, resource):
        self.lm=rm.open_resource(resource)
        self.name=name
        calib = np.genfromtxt('Calibration_'+name+'.txt',delimiter = '\t')
        self._spline = models.SplineModel(perfix = "spline_",xknots = calib[:,0])
        self._params = self._spline[-1].guess(calib[:,1],calib[:,0])
        self._sp_out = self._spline[-1].fit(calib[:,1],self._params[-1],x=calib[:,0])

    def level_to_volume(self,level):
        return self._sp_out.eval(self._params, x = level)
    
    def measure_level(self):
        self.lm.query('MEAS?')
        lev=self.lm.read().split(" ")[0]
        return lev
    
    def force_measure(self):
        self.lm.query('MEAS')
    
    def set_sample(self):
        self.lm.query('MODE S')
        self.lm.query('MEAS')
        
    def stb(self):
        self.lm.query('*STB?')
        return self.lm.read()
    
    def measurement_interval(self):
        self.lm.query('INTVL?')
        measinterval=self.lm.read()
        measinterval=int(measinterval.split(':')[0])*3600+int(measinterval.split(':')[1])*60+int(measinterval.split(':')[2]) #measurement interval in seconds
        return measinterval
    