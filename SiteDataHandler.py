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
      self.pageData = {}
      self.articleData = {}
      self.formData = {}
      self.settings = {'uiFramework':'onsen', 'pageType':'carousel', 'theme':'light', 'siteName':'', 'description':'', 'customTheme':'', 'pinataJWT':''}
      self.authors = {}
      self.uiFramework = ['onsen']
      self.navigation = ['carousel', 'splitter', 'tabs']
      self.themes = ['light', 'dark']
      self.dataFilePath = os.path.join(filePath, 'site.data')
      self.fileExists = False
      
      if os.path.isfile(self.dataFilePath):
          dataFile = open(self.dataFilePath, 'rb')
          data = pickle.load(dataFile)
          self.folders = data['folders']
          self.pageData = data['pageData']
          self.articleData = data['articleData']
          self.formData = data['formData']
          self.settings = data['settings']
          self.fileExists = True
      else:
          self.saveData()       
      
   def addFolder(self, folder, selfData):
       if(folder not in selfData):
           selfData[folder] = {}
           
   def updateData(self, folder, path, selfData, data):
       if(folder in selfData):
           selfData[folder][path] = data
       else:
           self.addFolder(folder, self.folders)
           self.updateData(folder, path, selfData, data)
           
   def updateFile(self, folder, path, uiType, active=True):
       if(folder in self.folders):
           data = {'path':path, "type":uiType, "active":active}
           self.updateData(folder, path, self.folders, data)
       else:
           self.addFolder(folder, self.folders)
           self.updateFile(folder, path, uiType, active)         
           
   def updatePageData(self, folder, path, data):
       if(folder in self.pageData):
           self.updateData(folder, path, self.pageData, data)
       else:
           self.addFolder(folder, self.pageData)
           self.updatePageData(folder, path, data)
           
   def updateArticleData(self, folder, path, data):
       if(folder in self.articleData):
           self.updateData(folder, path, self.articleData, data)
       else:
           self.addFolder(folder, self.articleData)
           self.updateArticleData(folder, path, data)
           
   def updateFormData(self, folder, path, data):
       if(folder in self.formData):
           self.updateData(folder, path, self.formData, data)
       else:
           self.addFolder(folder, self.formData)
           self.updateFormData(folder, path, data) 
           
   def updateSetting(self, setting, value):
       self.settings[setting] = value
       self.saveData()
       
   def getData(self, folder, path, selfData):
       result = None
       if(folder in selfData.keys() and path in selfData[folder].keys()):
           result = selfData[folder][path]
           
       return result
   
   def addAuthor(self, name, img):
       if name not in self.authors.keys():
           self.authors[name] = img
           
   def saveData(self):
       file = open(self.dataFilePath, 'wb')
       data = {'folders':self.folders, 'pageData':self.pageData, 'articleData':self.articleData, 'formData':self.formData, 'settings':self.settings, 'authors':self.authors}
       pickle.dump(data, file)
       file.close()
             
       

   
    


