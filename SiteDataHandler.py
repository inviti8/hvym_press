# -*- coding: utf-8 -*-
"""
Created on Mon Oct 10 11:18:11 2022

@author: meta-cronos

Initialize with and object containing folder-objects, each containing and array
with .md files contained in the folder:
    {
     'folder1':[md-file1, md_file2, md_file3,...etc],
     'folder2':[md-file1, md_file2, md_file3,...etc]
     }


"""
import os
import pickle

class SiteDataHandler:
   'Class for handling site data.'
   
   def __init__(self, filePath):
      self.folders = {}
      self.dataFilePath = os.path.join(filePath, 'site.data')
      self.data = None
      
      if os.path.isfile(self.dataFilePath):
          data = open(self.dataFilePath, 'rb')
          self.data = pickle.load(data)
      else:
          self.saveData()
          
      
   def addFolder(self, folder):
       if(folder not in self.folders):
           self.folders[folder] = []
           
   def updateFile(self, folder, path, uiType, active=True):
       if(folder in self.folders):
           folderData = {'path':path, "type":uiType, "active":active}
           self.folders[folder].append(folderData)
       else:
           self.addFolder(folder)
           self.updateFile(folder, path, uiType, active)
           
   def saveData(self):
       file = open(self.dataFilePath, 'wb')
       pickle.dump(self.folders, file)
       file.close()
             
       

   
    



