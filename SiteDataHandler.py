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
import json
import markdown
import jsonpickle
import pickle

class SiteDataHandler:
   'Class for handling site data.'
   
   def __init__(self, filePath):
      self.folders = {}
      self.pageData = {}
      self.columnWidths = {}
      self.articleData = {}
      self.formData = {}
      self.metaData = {}
      self.settings = {'uiFramework':'onsen', 'pageType':'carousel', 'theme':'light', 'siteName':'', 'description':'', 'customTheme':'', 'pinataJWT':''}
      self.authors = {}
      self.uiFramework = ['onsen']
      self.navigation = ['carousel', 'splitter', 'tabs']
      self.themes = ['light', 'dark']
      self.dataFilePath = os.path.join(filePath, 'site.data')
      self.fileExists = False
      self.oldDataFolders = []
      self.oldDataKeys = []
      
      if os.path.isfile(self.dataFilePath):
          dataFile = open(self.dataFilePath, 'rb')
          data = pickle.load(dataFile)
          self.folders = data['folders']
          self.pageData = data['pageData']
          self.columnWidths = data['columnWidths']
          self.articleData = data['articleData']
          self.formData = data['formData']
          self.metaData = data['metaData']
          self.settings = data['settings']
          self.authors = data['authors']
          self.fileExists = True
      else:
          self.saveData()       
      
   def addFolder(self, folder, selfData):
       result = False
       if(folder not in selfData):
           selfData[folder] = {}
           result = True
           
       return result
           
   def addPageAll(self, folder):
       print('This is called:')
       print(folder)
       result = False
       if self.addFolder(folder, self.pageData):
           result = True
       if self.addFolder(folder, self.columnWidths):
           result = True
           
       return result
       
   def addFolderAll(self, folder):
       result = False
       if self.addFolder(folder, self.folders):
           result = True
       if self.addFolder(folder, self.pageData):
           result = True
       if self.addFolder(folder, self.columnWidths):
           result = True
       if self.addFolder(folder, self.articleData):
           result = True
       if self.addFolder(folder, self.formData):
           result = True
       if self.addFolder(folder, self.metaData):
           result = True
           
       return result
   
   def hasNoFolder(self, folder):
        result = False
        if folder not in self.pageData.keys():
            result = True
            
        return result
    
   def hasNoFileFolder(self, folder):
       result = False
       if folder not in self.folders:
           result = True
       if folder not in self.articleData:
           result = True
       if folder not in self.formData:
           result = True
       if folder not in self.metaData:
           result = True
           
       return result
   
   def hasNoFile(self, folder, path):
        result = False
        if path not in self.folders[folder]:
            result = True
        if path not in self.articleData[folder]:
            result = True
        if path not in self.formData[folder]:
            result = True
        if path not in self.metaData[folder]:
            result = True
            
        return result
    
   def pruneFolder(self, folderArr, selfData):
       for k in selfData:
           if k not in folderArr:
               selfData.pop(k)
               
   def pruneFile(self, folder, fileArr, selfData):
       print(folder)
       if folder in selfData.keys():
           for k in selfData[folder]:
               print(k)
               if k not in fileArr and '.md' in k:
                   if selfData[folder] not in self.oldData:
                       print(k + " added to delete list")
                       self.oldData.append(selfData[folder])
                       self.oldDataFolders.append(folder)
                       self.oldDataKeys.append(k)
    
   def pruneFolders(self, folder, arr):
       self.pruneFolder(arr, self.folders)
       self.pruneFolder(arr, self.pageData)
       self.pruneFolder(arr, self.columnWidths)
       self.pruneFolder(arr, self.articleData)
       self.pruneFolder(arr, self.formData)
       self.pruneFolder(arr, self.metaData)
       
   def pruneFiles(self, folder, arr):
       self.pruneFile(folder, arr, self.folders)
       self.pruneFile(folder, arr, self.articleData)
       self.pruneFile(folder, arr, self.formData)
       self.pruneFile(folder, arr, self.metaData)
       
   def deleteFile(self, folder, path, selfData):
       if folder in selfData.keys() and path in selfData[folder].keys():
           selfData[folder].pop(path)
       
   def deleteOldData(self):
       idx = 0

       for folder in self.oldDataFolders:
           path = self.oldDataKeys[idx]
           
           self.deleteFile(folder, path, self.folders)
           self.deleteFile(folder, path, self.articleData)
           self.deleteFile(folder, path, self.formData)
           self.deleteFile(folder, path, self.metaData)

           idx += 1
           
       self.oldDataFolders.clear()
       self.oldDataKeys.clear()
           
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
           
   def updatePageData(self, folder, data):
       if(folder in self.pageData):
           self.pageData[folder] = data
       else:
           self.addFolder(folder, self.pageData)
           self.updatePageData(folder, data)
           
   def updateColumnWidths(self, folder, data):
       if(folder in self.columnWidths):
           self.columnWidths[folder] = data
       else:
           self.addFolder(folder, self.columnWidths)
           self.updateColumnWidths(folder, data)
           
   def updateArticleData(self, folder, path, data):
       if(folder in self.articleData):
           self.updateData(folder, path, self.articleData, data)
       else:
           self.addFolder(folder, self.articleData)
           self.updateArticleData(folder, path, data)
           
   def updateArticleHTML(self, folder, path, filePath):
       if(folder in self.articleData):
           file = open(filePath, 'rb')
           md_file = file.read()
           html = markdown.markdown(md_file)
           #print(html)
           self.articleData[folder][path]['html'] = html
           file.close()
           
   def updateFormData(self, folder, path, data):
       if(folder in self.formData):
           self.updateData(folder, path, self.formData, data)
       else:
           self.addFolder(folder, self.formData)
           self.updateFormData(folder, path, data)
           
   def updateMetaData(self, folder, path, data):
       if(folder in self.metaData):
           self.updateData(folder, path, self.metaData, data)
       else:
           self.addFolder(folder, self.metaData)
           self.updateMetaData(folder, path, data)
           
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
           
   def updateAuthor(self, name, img):
       if name in self.authors.keys():
           self.authors[name] = img
           
   def getJsonData(self):
       dataFile = open(self.dataFilePath, 'rb')
       data = pickle.load(dataFile)
       json_obj = jsonpickle.encode(data)
       print(json_obj)
           
   def saveData(self):
       file = open(self.dataFilePath, 'wb')
       data = {'folders':self.folders, 'pageData':self.pageData, 'columnWidths':self.columnWidths, 'articleData':self.articleData, 'formData':self.formData, 'metaData':self.metaData,'settings':self.settings, 'authors':self.authors}
       pickle.dump(data, file)
       file.close()
             
       

   
    



