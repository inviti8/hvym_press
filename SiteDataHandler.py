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
import pickle
import shutil
import markdown
import datetime
import jsonpickle
from pathlib import Path
from dataclasses import dataclass
from dataclasses_json import dataclass_json
from jinja2 import Environment, FileSystemLoader

SCRIPT_DIR = os.path.abspath( os.path.dirname( __file__ ) )
HOME_PATH = str(Path.home())
file_loader = FileSystemLoader('templates')
env = Environment(loader=file_loader)

@dataclass_json
@dataclass      
class pages:
    '''
    Creates data object to be used in jinja text renderer.
    :param name: String identifier name of element.
    :type name:  (str)
    :param title: Rendered title of element.
    :type title:  (str)
    :param columns: Object for column data.
    :type columns:  (Object)
    :return: (Object) Containing data elements
    :rtype: (Object)
    '''
    name: str
    title: str
    columns: []
    max_height: str
    footer_height: str
    
@dataclass_json
@dataclass      
class cards:
    '''
    Creates data object to be used in jinja text renderer.
    :param name: String identifier name of element.
    :type name:  (str)
    :param title: Rendered title of element.
    :type title:  (str)
    :param html: Rendered title of element.
    :type html:  (str)
    :param columns: Object for column data.
    :type columns:  (Object)
    :return: (Object) Containing data elements
    :rtype: (Object)
    '''
    name: str
    title: str
    html: str

class SiteDataHandler:
   'Class for handling site data.'
   
   def __init__(self, filePath):
      self.pageList = []
      self.folders = {}
      self.pageData = {}
      self.columnWidths = {}
      self.articleData = {}
      self.formData = {}
      self.metaData = {}
      self.settings = {'uiFramework':'onsen', 'pageType':'carousel', 'style':'default', 'deployType':'Pinata', 'theme':'light', 'siteName':'', 'description':'', 'customTheme':'', 'pinataJWT':'', 'arWallet':''}
      self.authors = {}
      self.uiFramework = ['onsen']
      self.navigation = ['carousel', 'splitter', 'tabs']
      self.themes = ['light', 'dark']
      self.styles = ['default', 'material']
      self.deployTypes = ['Pinata', 'Arweave']
      self.dataFilePath = os.path.join(filePath, 'site.data')
      self.fileExists = False
      self.oldFolders = []
      self.oldDataFolders = []
      self.oldDataKeys = []
      self.templateDebug = 'template_index.txt'
      
      if os.path.isfile(self.dataFilePath):
          dataFile = open(self.dataFilePath, 'rb')
          data = pickle.load(dataFile)
          self.pageList = data['pageList']
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
          
   def _renderPageTemplate(self, template_file, data, page):

       template = env.get_template(template_file)
       output = template.render(data=data)
       
       with open(page, "wb") as f:
           f.write(output.encode())
           
   def openStaticPage(self, template_file, data, route=0):
       '''
       Open model for debugging.
       routes are:
           0:/debug/
           1:/deploy/
       '''
       routes = ['debug', 'deploy']
       target_path = os.path.join(SCRIPT_DIR, 'serve', routes[route])
       page_path = os.path.join(target_path,'index.html')

       if route == 0:
           self._renderPageTemplate(template_file, data, page_path)
           
   def generateFormData(self, page, article):
       result = []
       form_data = self.formData[page][article]
       
       for k in form_data['formType'].keys():
           print('key is: '+k)
           if form_data['formType'][k] == True:
               print('adding input: ' + k)
               result.append(k)
           
       return result
           
   def generatePageData(self, page):
       result = {'title':None, 'max_height':None, 'columns':None, 'footer_height':None, 'content':{'columns':[], 'widths':self.columnWidths[page]}}
       for k in self.pageData[page].keys():
           result[k] = self.pageData[page][k]
       
       columns = int(self.pageData[page]['columns'])
       for idx in range(0, columns):
           result['content']['columns'].append([])
       
       for k in self.articleData[page].keys():
           article_data = { 'column':None, 'type':None, 'style':None, 'border':None, 'author':None, 'use_thumb':None, 'html':None, 'height':None, 'author_img':None, 'bg_img':None, 'form_data':[], 'form_html':"", 'form_btn_txt':"", 'form_response':"", 'form_id':""}
           props = self.articleData[page][k].keys()
           
           for prop in props:
               article_data[prop] = self.articleData[page][k][prop]
               
           author = self.articleData[page][k]['author']
           author_img = self.authors[author]
           article_data['author_img'] = author_img

           if article_data['type'] == 'Form':
               article_data['form_data'] = self.generateFormData(page, k)
               article_data['form_html'] = self.formData[page][k]['customHtml']
               article_data['form_btn_txt'] = self.formData[page][k]['btn_txt']
               article_data['form_response'] = self.formData[page][k]['response']
               article_data['form_id'] = self.formData[page][k]['form_id']
           index = int(article_data['column'])-1
           result['content']['columns'][index].append(article_data)
           
       return result
       
  
   def generateSiteData(self):
       result = {'pages':[], 'settings':self.settings}
       for page in self.pageList:
          page_data = self.generatePageData(page)
          result['pages'].append(page_data)
           
       return result
           
           
   
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

   def arrHasPartial(self, lst, query):
       result = False
       for s in lst:
           if query in s:
               result = True
               
       return result
           
   def pruneFolder(self, folderArr, selfData):
       if self.arrHasPartial(folderArr, ".md") == False and self.arrHasPartial(folderArr, ".png") == False:
           for k in selfData:
               if '.data' not in k and '.md' not in k and '.png' not in k and k not in folderArr:
                   if k not in self.oldFolders:
                       self.oldFolders.append(k)
                       print(k + " folder is added for delete.")
               
   def pruneFile(self, folder, fileArr, selfData):
       if folder in selfData.keys():
           for k in selfData[folder]:
               if k not in fileArr and '.md' in k:
                   if selfData[folder] not in self.oldData:
                       self.oldDataFolders.append(folder)
                       self.oldDataKeys.append(k)
    
   def pruneFolders(self, arr):
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
       
   def deleteFolder(self, folder, selfData):
       if folder in selfData.keys():
           selfData.pop(folder)
       
   def deleteFile(self, folder, path, selfData):
       if folder in selfData.keys() and path in selfData[folder].keys():
           selfData[folder].pop(path)
       
   def deleteOldFiles(self):
       idx = 0

       for folder in self.oldDataFolders:
           path = self.oldDataKeys[idx]
           
           self.deleteFile(folder, path, self.folders)
           self.deleteFile(folder, path, self.articleData)
           self.deleteFile(folder, path, self.formData)
           self.deleteFile(folder, path, self.metaData)

           idx += 1
           
       for folder in self.oldFolders:
           self.deleteFolder(folder, self.folders)
           self.deleteFolder(folder, self.pageData)
           self.deleteFolder(folder, self.columnWidths)
           self.deleteFolder(folder, self.articleData)
           self.deleteFolder(folder, self.formData)
           self.deleteFolder(folder, self.metaData)
           
       self.oldDataFolders.clear()
       self.oldDataKeys.clear()
       self.oldFolders.clear()
           
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
           file = open(filePath, 'r', encoding="utf-8")
           t = os.path.getmtime(filePath)
           md_file = file.read()
           md = markdown.Markdown()
           md.convert(md_file)
           #html = ""
           html = markdown.markdown(md_file)
           self.articleData[folder][path]['html'] = md.convert(html)
           self.articleData[folder][path]['time-stamp'] = t
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
           
   def deleteAuthor(self, author):
       for page in self.pageList:
          for k in self.articleData[page]:
              if self.articleData[page][k]['author'] == author:
                   self.articleData['author'] = "anonymous"          
                  
   def getJsonData(self):
       dataFile = open(self.dataFilePath, 'rb')
       data = pickle.load(dataFile)
       json_obj = jsonpickle.encode(data)
       print(json_obj)
           
   def saveData(self):
       file = open(self.dataFilePath, 'wb')
       data = {'pageList':self.pageList, 'folders':self.folders, 'pageData':self.pageData, 'columnWidths':self.columnWidths, 'articleData':self.articleData, 'formData':self.formData, 'metaData':self.metaData,'settings':self.settings, 'authors':self.authors}
       pickle.dump(data, file)
       file.close()
             
       

   
    



