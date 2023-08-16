import numpy as np
import datetime
import os

class SaveDat:
    def __init__(self,head,title,directory,notes):
        self.notes = notes
        self.head = head
        self.title = title
        self.directory = directory
        self.full_title = self.directory + '/'  + self.title + '.dat' #+ datetime.datetime.now().strftime("%y%m%d_%H") + 'h'
        #Create a new file by adding a number to the end (to avoid overwriting)
        if os.path.exists(self.full_title):
            mod=1
            while os.path.exists(self.full_title):
                self.full_title=self.directory + '/' +  self.title +'_'+str(mod)+ '.dat' #datetime.datetime.now().strftime("%y%m%d_%H") + 'h' +
                mod=mod+1
            
        with open(self.full_title,'w') as df:
            df.write(self.notes+'\n')
            df.write(self.head+'\n')
        
    def save_dat(self,X,Y):
        data = np.column_stack((X,Y))
        return np.savetxt(self.directory + '/' + datetime.datetime.now().strftime("%y%m%d_%H") + 'h' + self.title + '.dat', data, header=self.head,comments='',delimiter='\t')

    def save_dat3D(self,X,A, Y):
        data = np.column_stack((X,A,Y))
        return np.savetxt(self.directory + '/' + datetime.datetime.now().strftime("%y%m%d_%H") + 'h' + self.title + '.dat', data, header=self.head,comments='',delimiter='\t')

    def save_line(self,dat):
        #data=np.array(dat)
        df=open(self.full_title,'a')
        
        sdat=[str(x) for x in dat]
        
        line="\t".join(sdat)+'\n'

        #line=np.array2string(data,separator='\t',suffix='\n' )
        df.write(line)
        df.close()
     
    def save_txt_mean(self,X,Y,err):
        data = np.column_stack((X,Y,err))
        return np.savetxt(self.directory + '/' + datetime.datetime.now().strftime("%y%m%d_%H") + 'h' + self.title + '.dat', data, header=self.head,comments='',delimiter='\t')

    def save_txt_all(self,param):
        i=0;data=[]
        while i<len(param):
            data.append((param[i]))
            i+=1
        data=np.transpose(data)
        return np.savetxt(self.directory + '/' + datetime.datetime.now().strftime("%y%m%d_%H") + 'h' + self.title + '.dat', data, header=self.head,comments=self.notes+'\n',delimiter='\t')

class LogFile:
    
    def __init__(self, start, stop,iteration,directory):
        self.start = start
        self.stop = stop
        self.iteration = iteration
        self.directory = directory
        
    def ecrire(self):
        file = open(self.directory + '/' + datetime.datetime.now().strftime("%y%m%d-%H") + 'h' + '_Log.txt','w')
        file.write('Measurement started:' + self.start + '\n')
        file.write('Measurement finished:' + self.stop + '\n')
        file.write('Number of iteration:' + self.iteration + '\n')
        file.close()
                
class Folder:
   def __init__(self,directory):
       self.directory = directory

   def createFolder(self):
       try:
           if not os.path.exists(self.directory):
               os.makedirs(self.directory)
       except OSError:
           print ('Error: Creating directory. ' + self.directory)