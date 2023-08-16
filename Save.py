import os

class SaveDat:
    def __init__(self, directory, title, notes = None, header = None):
        '''
        Creates an object that correspond to a file with notes and header at the beginning. The object can append lines in the very file.
        
        Args:
            directory: a string telling the folder where the file should be saved
            title: a string telling the name of the files. Numbers will be appended to the name if the file already exists. 
            notes: a string written to the beginning of the file.
            header: an array that contains the header of the numpy table
        '''
        self.directory = directory
        self.title = title
        self.header = "\t".join(header)
        self.notes = notes
        
        self.filename = self.directory + '\\'  + self.title + '.dat' #+ datetime.datetime.now().strftime("%y%m%d_%H") + 'h'
        #Create a new file by adding a number to the end (to avoid overwriting)
        if os.path.exists(self.filename):
            mod=1
            while os.path.exists(self.filename):
                self.filename=self.directory + '\\' +  self.title +'_'+str(mod)+ '.dat' #datetime.datetime.now().strftime("%y%m%d_%H") + 'h' +
                mod=mod+1
            
        with open(self.filename,'w') as fw:
            if self.notes:
                fw.write('# '+self.notes+'\n')
            if self.header:
                fw.write(self.header+'\n')

    def saveLine(self,data):
        '''
        Append a line of data to the numpy table.
        Args:
            data: an array that include the data
        '''
        with open(self.filename,'a') as fa:
            sdat=[str(x) for x in data]
            line="\t".join(sdat)+'\n'
            fa.write(line)
        