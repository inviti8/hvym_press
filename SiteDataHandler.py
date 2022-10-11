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
      self.settings = {'siteName':'', 'pageType':'carousel', 'theme':'light'}
      self.navigation = ['carousel', 'splitter', 'tabs']
      self.themes = ['light', 'dark']
      self.dataFilePath = os.path.join(filePath, 'site.data')
      self.fileExists = False
      
      if os.path.isfile(self.dataFilePath):
          dataFile = open(self.dataFilePath, 'rb')
          data = pickle.load(dataFile)
          self.folders = data['folders']
          self.settings = data['settings']
          self.fileExists = True
      else:
          self.saveData()
          
      
   def addFolder(self, folder):
       if(folder not in self.folders):
           self.folders[folder] = {}
           
   def updateFile(self, folder, path, uiType, active=True):
       if(folder in self.folders):
           folderData = {'path':path, "type":uiType, "active":active}
           self.folders[folder][path] = folderData
       else:
           self.addFolder(folder)
           self.updateFile(folder, path, uiType, active)
           
   def updateSetting(self, setting, value):
       self.settings[setting] = value
       self.saveData()
           
   def saveData(self):
       file = open(self.dataFilePath, 'wb')
       data = {'folders':self.folders, 'settings':self.settings}
       pickle.dump(data, file)
       file.close()
             
       

   
    



