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
import time
import pickle
import shutil
import markdown
import jsonpickle
import MarkdownHandler
import W3DeployHandler
from pathlib import Path
from bs4 import BeautifulSoup
from jinja2 import Environment, FileSystemLoader



SCRIPT_DIR = os.path.abspath( os.path.dirname( __file__ ) )
HOME_PATH = str(Path.home())
file_loader = FileSystemLoader('templates')
env = Environment(loader=file_loader)


class SiteDataHandler:
   'Class for handling site data.'
   def __init__(self, filePath):
      self.filePath = filePath
      self.resourcePath = os.path.join(self.filePath, '_resources')
      self.pageList = []
      self.folders = {}
      self.pageData = {}
      self.columnWidths = {}
      self.articleData = {}
      self.formData = {}
      self.metaData = {}
      self.settings = {'uiFramework':'onsen', 'pageType':'carousel', 'style':'default', 'row_pad':5, 'deployType':'Pinata', 'theme':'light', 'siteName':'', 'description':'', 'customTheme':'','pinata_jwt':'', 'pinata_key':'', 'pinata_gateway':'', 'pinata_meta_data':'', 'arWallet':''}
      self.authors = {}
      self.uiFramework = ['onsen']
      self.navigation = ['carousel', 'splitter', 'tabs']
      self.themes = ['light', 'dark']
      self.styles = ['default', 'material']
      self.deployTypes = ['Pinata', 'Arweave']
      self.dataFilePath = os.path.join(filePath, 'site.data')
      self.fileExists = False
      self.resourcesExist = False
      self.oldFolders = []
      self.oldDataFolders = []
      self.oldDataKeys = []
      self.templateDebug = 'template_index.txt'
      self.markdownHandler = MarkdownHandler.MarkdownHandler(filePath)
      self.debugPath = os.path.join(SCRIPT_DIR, 'serve', 'debug')
      self.debugResourcePath = os.path.join(SCRIPT_DIR, 'serve', '_resources')
      self.deployHandler = W3DeployHandler.W3DeployHandler(self.filePath, self.debugPath, self.resourcePath, self.settings)
      self.images = {}
      self.videos = {}
      self.audio = {}
      self.gltf = {}
      self.gatherMedia()
      
      if(os.path.isdir(self.resourcePath)):
          self.resourcesExist = True
      
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
          self.deployHandler = W3DeployHandler.W3DeployHandler(self.filePath, self.debugPath, self.resourcePath, self.settings)
          self.images = data['media']['images']
          self.videos = data['media']['videos']
          self.audio = data['media']['audio']
          self.gltf = data['media']['gltf']
 
      self.saveData()  
           
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
           self.markdownHandler.renderPageTemplate(template_file, data, page_path)
           
   def generateFormData(self, page, article):
       result = []
       form_data = self.formData[page][article]
       
       for k in form_data['formType'].keys():
           if form_data['formType'][k] == True:
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
           article_data = { 'column':None, 'type':None, 'style':None, 'border':None, 'max_width':None, 'author':None, 'use_thumb':None, 'html':None, 'height':None, 'author_img':None, 'bg_img':None, 'form_data':[], 'form_html':"", 'form_btn_txt':"", 'form_response':"", 'form_id':"", 'images':[], 'videos':[]}
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
   
   def baseFolder(self, f_path):
       sep = os.path.sep
       arr = f_path.split(sep)
       return(arr[len(arr)-2])
   
   def addFolder(self, folder, selfData):
       result = False
       if(folder not in selfData):
           selfData[folder] = {}
           result = True
           
       return result
           
   def addPageAll(self, folder):
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
           
   def cloneDirectory(self, source, target):
       source_files = os.listdir(source)
       target_files = os.listdir(target)
       
       for f in target_files:
           f_path = os.path.join(target, f)
           os.remove(f_path)
           
       for f in source_files:
            src_path = os.path.join(source, f)
            dst_path = os.path.join(target, f)
            shutil.copy(src_path, dst_path)
   
   def refreshDebugMedia(self):
       self.cloneDirectory(self.resourcePath, self.debugResourcePath)
        
   def deleteOldFiles(self):
       idx = 0

       for folder in self.oldDataFolders:
           path = self.oldDataKeys[idx]
           
           self.deleteFile(folder, path, self.folders)
           self.deleteFile(folder, path, self.articleData)
           self.deleteFile(folder, path, self.formData)
           self.deleteFile(folder, path, self.metaData)
           
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
       
   def mediaSaved(self, file_name):
       result = False
       if file_name in self.images.keys() or file_name in self.videos.keys() or file_name in self.audio.keys() or file_name in self.gltf.keys():
           result = True
           
       return result 

   def mediaOutOfDate(self, file_name, m_type):
       result = False
       media = {'images':self.images, 'videos':self.videos, 'audio':self.audio, 'gltf':self.gltf}

       if file_name in media[m_type].keys():
           path = media[m_type][file_name]['path']
           time_stamp = media[m_type][file_name]['time_stamp']
               
           if self.fileIsNew(path, time_stamp):
               result = True
               
       return result
       
   def fileList(self, ext):
       result = {}
       media = {'images':self.images, 'videos':self.videos, 'audio':self.audio, 'gltf':self.gltf}
       files = os.listdir(self.resourcePath)
       m_type = 'image'
       
       if ext == '.mp4':
           m_type = 'video'
       elif ext == '.mp3':
           m_type = 'audio'
       elif ext == '.gltf':
           m_type = '3d'
       
       for f in files:
           f_path = os.path.join(self.resourcePath, f)
           t_stamp = time.strftime("%b %d %H:%M:%S %Y", time.gmtime(os.path.getmtime(f_path)))
           obj = {'type':m_type, 'path':f_path, 'cid':None, 'time_stamp':t_stamp}
           key = 'images'

           if m_type == 'video':
               key = 'videos'
           elif m_type == 'audio':
               key = 'audio'
           elif m_type == '3d':
               key = 'gltf'
               
           if os.path.isfile(f_path) and ext in f:
               if self.mediaSaved(f) == False or self.mediaOutOfDate(f, key) == True:
                   result[f] = obj

               else:
                   if m_type == 'image':
                       result[f] = media['images'][f]
                   elif m_type == 'video':
                       result[f] = media['videos'][f]
                   elif m_type == 'audio':
                       result[f] = media['audio'][f]
                   elif m_type == '3d':
                       result[f] = media['gltf'][f]
               
       return result
   
   def fileIsNew(self, filePath, time_stamp):
       result = False
       t = time.strftime("%b %d %H:%M:%S %Y", time.gmtime(os.path.getmtime(filePath)))
       latest = max((t, time_stamp))
       
       if t == latest and t != time_stamp:
           result = True
       
       return result
   
   def deployMedia(self, usefullPath=False, askPermission=True):
       result = False
       
       result = self.deployHandler.pinataDirectoryGUI(self.resourcePath, True, True, usefullPath, askPermission)
       self.deployHandler.saveData()
       
       return result
   
   def deploySite(self, usefullPath=False, askPermission=True):
        result = False
        
        result = self.deployHandler.pinataDirectoryGUI(self.debugPath, True, True, usefullPath, askPermission)
        self.deployHandler.saveData()
        
        return result
   
   def gatherMedia(self):
       self.images = self.fileList('.png')
       self.videos = self.fileList('.mp4')
       self.audio = self.fileList('.mp3')
       self.gltfs = self.fileList('.gltf')
       
       return{'images':self.images, 'videos':self.videos, 'audio':self.audio, 'gltf':self.gltf}
           
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
           t = time.strftime("%b %d %H:%M:%S %Y", time.gmtime(os.path.getmtime(filePath)))
           
           if self.deployHandler.manifest != None:
               self.markdownHandler.deployerManifest = self.deployHandler.manifest
           
           self.articleData[folder][path]['html'] = self.markdownHandler.generateHTML(filePath)
           self.articleData[folder][path]['time_stamp'] = t
           
   def updateAllArticleHTML(self, folder):
       files = os.listdir(folder)
       
       for f in files:
           fullname = os.path.join(folder, f)
           f_name = os.path.basename(f)
           f_path = self.baseFolder(fullname.replace(f_name, ''))
           
           if os.path.isdir(fullname):
               self.updateAllArticleHTML(fullname)
           else:
               self.updateArticleHTML(f_path, f_name, fullname)
           
   def updateMediaFiles(self, folder, path, filePath):
       if(folder in self.articleData):
           html = self.articleData[folder][path]['html']
           media = self.gatherMedia()
           soup = BeautifulSoup(html, 'html.parser')
           html_imgs = soup.find_all('img')
           html_vids = soup.find_all('video')
           
           for image in media['images']:
               i_name = os.path.basename(image)
           
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
       data = {'pageList':self.pageList, 'folders':self.folders, 'pageData':self.pageData, 'columnWidths':self.columnWidths, 'articleData':self.articleData, 'formData':self.formData, 'metaData':self.metaData,'settings':self.settings, 'authors':self.authors, 'media':self.gatherMedia()}
       pickle.dump(data, file)
       file.close()
             
       

   
    



