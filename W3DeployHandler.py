# -*- coding: utf-8 -*-
"""
Created on Tue Nov  8 13:27:01 2022

@author: meta-cronos

A class for handling web content deployment.

Sample Path:
https://sapphire-giant-butterfly-891.mypinata.cloud/ipfs/bafybeiapx5hzywrsw76v7dd6s5bvpta3djad65ovfrrwvs2367ul7kokde/DALL%C2%B7E%202022-10-03%2014.20.02%20-%20A%20digital%20illustratio.png
"""

import os
import time
import sys
import json
import pickle
import requests
import markdown
import threading
from PIL import Image
from json import dumps
from pathlib import Path
import PySimpleGUI as sg
from dataclasses import dataclass
from dataclasses_json import dataclass_json
from dataclasses import dataclass, asdict, field
from jinja2 import Environment, FileSystemLoader

SCRIPT_DIR = os.path.abspath( os.path.dirname( __file__ ) )
HOME_PATH = str(Path.home())
file_loader = FileSystemLoader('templates')
env = Environment(loader=file_loader)

@dataclass_json
@dataclass      
class pinata_payload:
    '''
    Creates data object for rendering the static page route from template.
    :param name: name of file'
    :type name:  (str)
    :param path: path of file'
    :type path:  (str)
    :param fileType: string for file type, as image/svg+xml:'
    :type fileType:  (str)
    :param wrapWithDirectory: if file is in directory or not.'
    :type wrapWithDirectory:  (bool)
    :param pinToIPFS: Pin file or dont.'
    :type pinToIPFS:  (bool)
    :param pinataMetadata: related metadata json string
    :type pinataMetadata:  (str)
    :return: (Object) Containing data elements
    :rtype: (Object)
    '''
    pinataOptions: str
    name: str
    path: str
    wrapWithDirectory: str
    pinToIPFS: str
    pinataMetadata:str
    
    @property
    def dictionary(self):
        return asdict(self)

    @property
    def json(self):
        return dumps(self.dictionary)
    
@dataclass_json
@dataclass      
class pinata_submarine_payload:
    '''
    Creates data object for rendering the static page route from template.
    :param name: name of file'
    :type name:  (str)
    :param path: path of file'
    :type path:  (str)
    :param fileType: string for file type, as image/svg+xml:'
    :type fileType:  (str)
    :param wrapWithDirectory: if file is in directory or not.'
    :type wrapWithDirectory:  (bool)
    :param pinToIPFS: Pin file or dont.'
    :type pinToIPFS:  (bool)
    :param pinataMetadata: related metadata json string
    :type pinataMetadata:  (str)
    :return: (Object) Containing data elements
    :rtype: (Object)
    '''
    name: str
    wrapWithDirectory: str
    pinToIPFS: str
    metadata:str
    
    @property
    def dictionary(self):
        return asdict(self)

    @property
    def json(self):
        return dumps(self.dictionary)


class W3DeployHandler:
   """
   Class for handling deploy data,
   and deployment of files.
   
   """
   
   def __init__(self, filePath, sitePath, resourcePath, settings):
       self.resourcePath = resourcePath
       self.siteName = settings['siteName']
       self.siteID = settings['siteID']
       self.sitePath = sitePath
       self.files = None
       self.dataFilePath = os.path.join(filePath, 'deploy.data')
       self.manifest = {}
       self.pinataPinURL = 'https://api.pinata.cloud/pinning'
       self.pinataSubmarineURL = 'https://managed.mypinata.cloud/api/v1/content'
       self.pinataDataURL = 'https://api.pinata.cloud/data'
       self.pinata = {'api_url':"https://managed.mypinata.cloud/api/v1/content", 'jwt':settings['backend_auth_key'], 'api_key':settings['pinata_key'], 'gateway':settings['backend_end_point'], 'timeout':settings['backend_timeout'], 'meta_data':settings['backend_meta_data']}
       self.pinataToken = None
       self.deployFiles = []
       self.deployedStatuses = {}
       self.deployFolderName = ''
       self.maxCalls = 5
       self.usedCalls = self.maxCalls
       self.folderCID = None
       self.folderID = None
       self.deployedUrl = None
       
       if os.path.isdir(self.resourcePath):
           self.files = os.listdir(self.resourcePath)
       
       if os.path.isfile(self.dataFilePath):
           dataFile = open(self.dataFilePath, 'rb')
           data = pickle.load(dataFile)
           self.manifest = data['manifest']
           self.pinata = data['pinata']

       self.updateManifestData(filePath)
       
       
   def _privateFolderDeploymentChecker(self, window):
        print('_privateFolderDeploymentChecker')
        result = False
        responses = []
        
        while self.folderCID == None:
            time.sleep(1)
            if self.usedCalls > 0:
                self._privateFolderDeploymentChecker(window)
            
        list_url = os.path.join(self.pinataSubmarineURL, self.folderID, 'list').replace('\\', '/')
        
        payload = {}
        
        headers = {
          'x-api-key': self.pinata['api_key']
        }
        
        response = requests.request("GET", list_url, headers=headers, data=payload)
        
        if response.status_code == 200:
            items = response.json().get('items')
  
            for f in self.deployFiles:
                f_name = f[1][0]
                f_name = f_name = "/".join(f_name.strip("/").split('/')[1:])
                f_key = os.path.basename(f_name)
                url = None
                
                for item in items:
                    if f_key in item['originalname']:
                        time.sleep(1)
                        token = self.generatePinataToken([item['id']], self.pinata['timeout']).strip('"')
                        gateway = 'https://'+self.pinata['gateway']
                        url = os.path.join((item['uri']+'?accessToken=')).replace('\\', '/')
                        url = gateway+url+token
                        #self.updateFileDataPinataURL(f_key, url)
                        self.pinataFileDataURL(f_key, url)
                        self.folderCID = url
                        self.pinataToken = token
                        if 'index.html' in f_key:
                            self.deployedUrl = url
        
        if window != None and window.write_event_value != None:
            window.write_event_value('Exit', '')
            self.saveData()
            sys.exit()
            
       
   def _folderDeploymentChecker(self, window):
            
        while self.folderCID == None:
            time.sleep(1)
            if self.usedCalls > 0:
                self._folderDeploymentChecker(window,)
            
        #Deploy index first, if it's there
        if self.deployedUrl == None:
            for f in self.deployFiles:
                f_name = f[1][0]
                f_name = f_name = "/".join(f_name.strip("/").split('/')[1:])
                f_key = os.path.basename(f_name)

                if 'index.html' in f_key and f_key not in self.deployedStatuses.keys():
                    url = os.path.join('https://', self.pinata['gateway'], 'ipfs', self.folderCID, f_name).replace('\\', '/')
                    response = requests.get(url)
                    self.usedCalls -= 1
                    self.deployedStatuses[f_key] = response.status_code
                    self.deployedUrl = url
       
        for f in self.deployFiles:
            time.sleep(1)
            f_name = f[1][0]
            f_name = f_name = "/".join(f_name.strip("/").split('/')[1:])
            f_key = os.path.basename(f_name)
            url = os.path.join('https://', self.pinata['gateway'], 'ipfs', self.folderCID, f_name).replace('\\', '/')
            
            #self.updateFileDataPinataURL(f_key, url)
            self.pinataFileDataURL(f_key, url)
            
            if self.usedCalls > 0 and 'index.html' not in f:
                if f_key not in self.deployedStatuses.keys():
                    response = requests.get(url)
                    self.usedCalls -= 1
                    self.deployedStatuses[f_key] = response.status_code
                    
                else:
                    if self.deployedStatuses[f_key] != 200:
                        response = requests.get(url)
                        self.usedCalls -= 1
                        self.deployedStatuses[f_key] = response.status_code
  
        for key, value in self.deployedStatuses.items():
            if value != 200 and self.usedCalls > 0:
                self._folderDeploymentChecker(window,)
               
        self.deployFiles.clear()
        self.deployedStatuses.clear()
        self.usedCalls = self.maxCalls
       
        if window != None and window.write_event_value != None:
            window.write_event_value('Exit', '')
            self.saveData()
            sys.exit()
            
       
   def _folderArray(self, key, parentPath, filePath, basePath, window=None):
       paths = os.listdir(filePath)
       
       for f in paths:
           full_path = os.path.join(filePath, f).replace('\\', '/')
           f_name = full_path.replace(basePath, '').replace('\\', '/')
           f_name = os.path.join(self.siteID+'_'+f_name, f_name).replace('\\', '/')
           
           if self.deployFolderName != '':
               arr = f_name.split('/')
               folder = arr[len(arr)-2]
               f_name = f_name.replace(folder, self.deployFolderName)
           
           if os.path.isdir(full_path):
               self._folderArray(key, full_path, full_path, basePath, window)
           else:
               self.deployFiles.append((key,(f_name,open(full_path,'rb'),'application/octet-stream')))
               
               
   def generatePinataToken(self, contentIdArr, timeOutSecs):
       print('Generating Pinata Access Token')
       url = os.path.join("https://managed.mypinata.cloud/api/v1/auth/content/jwt")

       payload = json.dumps({
          "timeoutSeconds": timeOutSecs,
          "contentIds": contentIdArr
        })
       headers = {
          'x-api-key': self.pinata['api_key'],
          'Content-Type': 'application/json'
        }
        
       response = requests.request("POST", url, headers=headers, data=payload)
       
       print('Token gen response code:')
       print(response.status_code)
       
       return response.text
       
   def submarineFiles(self, files, payload, window=None):
        url = self.pinataSubmarineURL

        headers = {
          'x-api-key': self.pinata['api_key']
        }
       
        if window != None:
            threading.Thread(target=self._privateFolderDeploymentChecker,
                              args=(window, ),
                              daemon=True).start()
        response = requests.request("POST", url, headers=headers, data=payload, files=files)
        
        print(response.text)
        
        if response.status_code == 200:
            data = json.loads(response.text).get('items')[0]
            
            self.folderCID = data['cid']
            self.folderID = data['id']
       
        return response

                   
   def pinataFiles(self, files, payload, window=None):
        url = os.path.join(self.pinataPinURL, 'pinFileToIPFS').replace('\\', '/')
        
        headers = {
          'Authorization': "Bearer "+self.pinata['jwt']
        }
       
        if window != None:
            threading.Thread(target=self._folderDeploymentChecker,
                              args=(window, ),
                              daemon=True).start()
       
        response = requests.request("POST", url, headers=headers, data=payload, files=files)
        
        print(response.text)
       
        self.folderCID = response.json().get('IpfsHash')
       
        return response
       
       
   def pinataFile(self, filePath, payload):
       result = False
       f_name = os.path.basename(filePath)
       arr = filePath.split('/')
       parent_folder = arr[len(arr)-2]
       fileName = os.path.join(parent_folder, f_name).replace('\\', '/')
       
       if len(self.pinata['jwt'])>0 and len(self.pinata['gateway'])>0:
            url = os.path.join(self.pinataPinURL, 'pinFileToIPFS').replace('\\', '/')
            
            headers = {
              'Authorization': "Bearer "+self.pinata['jwt']
            }
    
            files=[
              ('file',(fileName,open(filePath,'rb'), 'application/octet-stream'))
            ]
           
            response = requests.request("POST", url, headers=headers, data=payload.dictionary, files=files)
           
            if response.status_code == 200:
                cid = response.json().get('IpfsHash')
                url = os.path.join('https://', self.pinata['gateway'], 'ipfs', cid, f_name).replace('\\', '/')
                result = url
       else:
             print('Pinata Credentials Not Set!')
             
       return result
   
   def pinataCss(self, filePath):
       metadata = self.pinata['meta_data']
       f_name = os.path.basename(filePath)
       arr = filePath.split('/')
       parent_folder = arr[len(arr)-2]
       fileName = os.path.join(parent_folder, f_name).replace('\\', '/')

       payload = pinata_payload('{"cidVersion": 1}', fileName, filePath, 'true', 'true', metadata)
       
       return self.pinataFile(filePath, payload)  
       
   
   def pinataDirectory(self, filePath, wrapWithDirectory=True, pinToIPFS=True, useParentDirs=False):
       result = False
       if len(self.pinata['jwt'])>0 and len(self.pinata['gateway'])>0:
           root_folder = os.path.basename(filePath)
           base_path = filePath.replace(root_folder, '').replace('\\', '/')
           if useParentDirs:
               drive_tail = os.path.splitdrive(base_path)
               base_path = drive_tail[0].replace('\\', '/')
               
           metadata = self.pinata['meta_data']
           payload = pinata_payload('{"cidVersion": 1}', root_folder, filePath, wrapWithDirectory, pinToIPFS, metadata)
           self.deployFiles.clear()
           self._folderArray('', filePath, base_path)
           
           response = self.pinataFiles(self.deployFiles, payload.dictionary)
           
           if response.status_code == 200:
               result = True
       else:
            print('Pinata Credentials Not Set!')
            
       return result
       
   def pinataDirectoryGUI(self, filePath, wrapWithDirectory=True, pinToIPFS=True, useParentDirs=False, askPermission=True, private=False):
       result = None
       popup = 'OK'
       message = 'Deploy Site to ipfs?'
       if private:
           message = 'Submarine Site?'
           
       if askPermission == True:
           popup = sg.popup_ok_cancel(message)
           
       if popup == 'OK':
           if len(self.pinata['jwt'])>0 and len(self.pinata['gateway'])>0:
               root_folder = os.path.basename(filePath)
               base_path = filePath.replace(root_folder, '').replace('\\', '/')
               if useParentDirs==True:
                   drive_tail = os.path.splitdrive(base_path)
                   base_path = drive_tail[0].replace('\\', '/')
                   
               metadata = self.pinata['meta_data']
               payload = pinata_payload('{"cidVersion": 1}', root_folder, filePath, str(wrapWithDirectory).lower(), str(pinToIPFS).lower, metadata)
               
               layout = [[sg.Text('Deploying Files:')],
                          [sg.ProgressBar(max_value=10, orientation='h', size=(20, 20), key='progress_1')]]
        
               ring_gray_segments = b'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'

               gif = ring_gray_segments
               
               layout = [[sg.Image(data=gif, enable_events=True, background_color='white', key='-IMAGE-', right_click_menu=['UNUSED', ['Exit']], pad=0)],]
        
               window = sg.Window('Deploy', layout,
                       no_titlebar=True,
                       grab_anywhere=False,
                       keep_on_top=True,
                       #background_color='white',
                       transparent_color='white' if sg.running_windows() else None,
                       alpha_channel=.8,
                       margins=(0,0))
               
               deploy_method = self.pinataFiles
               key = 'file'

               if private == True:
                   print("this is a submarine call")
                   deploy_method = self.submarineFiles
                   key = 'files'
                   payload = pinata_submarine_payload(root_folder, 'true', 'false', metadata)
                   
               self._folderArray(key, '', filePath, base_path)
                   
        
               threading.Thread(target=deploy_method,
                                 args=(self.deployFiles, payload.dictionary, window),
                                 daemon=True).start()
               
               while True:                                     # Event Loop
                   event, values = window.read(timeout=10)    # loop every 10 ms to show that the 100 ms value below is used for animation
                   if event == 'Exit':
                             break
                   if event in (sg.WIN_CLOSED, 'Exit', 'Cancel'):
                       break
                   # update the animation in the window
                   window['-IMAGE-'].update_animation(gif,  time_between_frames=100)
                   
               result = (self.folderCID, self.deployedUrl)
               
               self.folderCID = None
               self.folderID = None
               self.pinataToken = None
               self.deployedUrl = None
               self.deployFolderName = ''
               self.deployFiles.clear() 
               window.close()
           else:
               sg.popup_ok('Pinata Credentials Not Set!')
               
           return result
       
   def pinataResourcesGUI(self, wrapWithDirectory=True, pinToIPFS=True, useParentDirs=False):
       self.pinataDirectoryGUI(self.resourcePath, wrapWithDirectory, pinToIPFS, useParentDirs)
       
   def newFileData(self, filePath):
       return {'time_stamp':'', 'type':None, 'path':filePath, 'url':None, 'items':[]}
   
   def updateFileDataPinataID(self, filePath, i_d):
       f_name = os.path.basename(filePath)
       if f_name in self.manifest.keys():
           self.manifest[f_name]['id'] = i_d
           
   def pinataFileDataURL(self, f_key, url):
       if f_key in self.manifest.keys():
           print('the url is being saved for: '+f_key)
           print(url)
           self.manifest[f_key]['url'] = url
           self.saveData()
   
   def updateFileDataPinataURL(self, filePath, url):
       f_name = os.path.basename(filePath)
       if f_name in self.manifest.keys():
           self.manifest[f_name]['url'] = url
   
   def updateManifestData(self, filePath):
       files = os.listdir(filePath)
       prune_data = []
       for f in files:
           f_name = os.path.basename(f)
           f_path = os.path.join(filePath, f)
           
           if '.data' not in f_name and '.md' not in f_name:
               if os.path.isfile(f_path):
                   if f_name not in self.manifest.keys():
                       self.manifest[f_name] = self.newFileData(f_path)
                   
               else:
                   self.updateManifestData(f_path)
                   
       for k in self.manifest.keys():
             if k not in files:
                 prune_data.append(k)
      
       self.saveData()
           
   def updateSettings(self, settings):
       self.pinata = {'api_url':"https://managed.mypinata.cloud/api/v1/content", 'jwt':settings['backend_auth_key'], 'api_key':settings['pinata_key'], 'gateway':settings['backend_end_point'], 'timeout':settings['backend_timeout'], 'meta_data':settings['backend_meta_data']}
       self.saveData()
       
   def setPinataApiKey(self, api_key):
       self.pinata['api_key'] = api_key
       
   def saveData(self):
       file = open(self.dataFilePath, 'wb')
       data = {'manifest':self.manifest, 'pinata':self.pinata}
       pickle.dump(data, file)
       file.close()

