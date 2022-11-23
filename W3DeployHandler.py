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
    wrapWithDirectory: False
    pinToIPFS: False
    pinataMetadata:str
    
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
       self.sitePath = sitePath
       self.files = os.listdir(self.resourcePath)
       self.dataFilePath = os.path.join(filePath, 'deploy.data')
       self.manifest = {}
       self.pinataPinURL = 'https://api.pinata.cloud/pinning'
       self.pinataDataURL = 'https://api.pinata.cloud/data'
       self.pinata = {'api_url':"https://managed.mypinata.cloud/api/v1/content", 'jwt':settings['pinata_jwt'], 'api_key':settings['pinata_key'], 'gateway':settings['pinata_gateway']}
       self.deployFiles = []
       self.folderCID = None
       
       if os.path.isfile(self.dataFilePath):
           dataFile = open(self.dataFilePath, 'rb')
           data = pickle.load(dataFile)
           self.manifest = data['manifest']
           self.pinata = data['pinata']

       self.updateManifestData(filePath)
       
       # print(self.files)
       # print(self.manifest)
       # print(self.pinata)
       
   def _folderDeploymentChecker(self, window):
       result = False
       responses = []
       
       while self.folderCID == None:
           time.sleep(1)
           self._folderDeploymentChecker(window)
       
       for f in self.deployFiles:
           time.sleep(1)
           f_name = f[1][0]
           f_name = os.path.basename(f_name)
           url = os.path.join('https://', self.pinata['gateway'], 'ipfs', self.folderCID, f_name).replace('\\', '/')
           
           response = requests.get(url)
           responses.append(response.status_code)
           
       for r in responses:
           if r != 200:
               self._folderDeploymentChecker(window)
             

       if window != None and window.write_event_value != None:
           window.write_event_value('Exit', '')
           sys.exit()
       
       
   def _folderArray(self, parentPath, filePath, basePath, window=None):
       paths = os.listdir(filePath)
       data_size = len(paths)
       idx = 0
       
       for f in paths:
           full_path = os.path.join(filePath, f).replace('\\', '/')
           f_name = full_path.replace(basePath, '').replace('\\', '/')
           
           if os.path.isdir(full_path):
               self._folderArray(full_path, full_path, basePath)
           else:
               self.deployFiles.append(('file',(f_name,open(full_path,'rb'),'application/octet-stream')))
       if window != None:
            window.write_event_value('update_progress_1', idx)
            idx+=1
            
               
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
       
       print(response)
       print(response.text)
       self.folderCID = response.json().get('IpfsHash')
       
       return response.text
       
       
   def pinataFile(self, fileName, filePath, fileType, payload):
       url = os.path.join(self.pinataPinURL, 'pinFileToIPFS').replace('\\', '/')

       files=[
         ('file',(fileName,open(filePath,'rb'),fileType))
       ]
       headers = {
         'Authorization': "Bearer "+self.pinata['jwt']
       }
       
       response = requests.request("POST", url, headers=headers, data=payload, files=files)
       
       return response.text
   
   def pinataDirectory(self, filePath, wrapWithDirectory=True, pinToIPFS=True, useParentDirs=False):
       root_folder = os.path.basename(filePath)
       #base_path = filePath.replace(root_folder, '')
       base_path = os.path.basename(os.path.normpath(filePath))
       if useParentDirs:
           drive_tail = os.path.splitdrive(base_path)
           base_path = base_path.replace(drive_tail[0], '')
       metadata = '{"keyvalues": { "example": "value" }}'
       payload = pinata_payload('{"cidVersion": 1}', root_folder, filePath, wrapWithDirectory, pinToIPFS, metadata)
       self.deployFiles.clear()
       self._folderArray('', filePath, base_path)
       
       self.pinataFiles(self.deployFiles, payload.dictionary)
       
   def pinataDirectoryGUI(self, filePath, wrapWithDirectory=True, pinToIPFS=True, useParentDirs=False):
       root_folder = os.path.basename(filePath)
       base_path = filePath.replace(root_folder, '').replace('\\', '/')
       #base_path = os.path.basename(os.path.normpath(root_folder))
       if useParentDirs==True:
           drive_tail = os.path.splitdrive(base_path)
           base_path = base_path.replace(drive_tail[0], '')
           
       print(base_path)
       print(root_folder)
       print(filePath)
       metadata = '{"keyvalues": { "example": "value" }}'
       payload = pinata_payload('{"cidVersion": 1}', root_folder, filePath, wrapWithDirectory, pinToIPFS, metadata)
       
       layout = [[sg.Text('Testing progress bar:')],
                  [sg.ProgressBar(max_value=10, orientation='h', size=(20, 20), key='progress_1')]]

       main_window = sg.Window('Test', layout, finalize=True)
       current_value = 1
       main_window['progress_1'].update(current_value)
       
       self.deployFiles.clear()
       self.folderCID = None
       self._folderArray('', filePath, base_path, main_window)
       
       print(self.deployFiles)

       threading.Thread(target=self.pinataFiles,
                         args=(self.deployFiles, payload.dictionary, main_window, ),
                         daemon=True).start()

       while True:
            window, event, values = sg.read_all_windows()
            if event == 'Exit':
                break
            if event.startswith('update_'):
                print(f'event: {event}, value: {values[event]}')
                key_to_update = event[len('update_'):]
                window[key_to_update].update(values[event])
                window.refresh()
                continue
            # process any other events ...
       window.close()

   def another_function(window):
       import time
       import random
       for i in range(10):
           time.sleep(2)
           current_value = random.randrange(1, 10)
           window.write_event_value('update_progress_1', current_value)
       time.sleep(2)
       window.write_event_value('Exit', '')
       
   def newFileData(self, filePath):
       f_type = None
       return {'time_stamp':'', 'type':f_type, 'path':filePath, 'url':None}
   
   def updateFileDataPinataURL(self, filePath, cid):
       f_name = os.path.basename(filePath)
       if f_name in self.manifest.keys():
           self.manifest[f_name]['url'] = os.path.join('https:/', self.pinata['gateway'], 'ipfs', cid, f_name)
   
   def updateManifestData(self, filePath):
       files = os.listdir(filePath)
       prune_data = []
       for f in files:
           f_name = os.path.basename(f)
           f_path = os.path.join(filePath, f)
           
           if f_name not in self.manifest.keys():
               if f_name != 'deploy.data':
                   self.manifest[f_name] = self.newFileData(f_path)
               
       for k in self.manifest.keys():
            if k not in files:
                prune_data.append(k)
                
       for k in prune_data:
           self.manifest.pop(k)
           
       self.saveData()
           
   def updateSettings(self, settings):
       self.pinata = {'api_url':"https://managed.mypinata.cloud/api/v1/content", 'jwt':settings['pinata_jwt'], 'api_key':settings['pinata_key'], 'gateway':settings['pinata_gateway']}
       self.saveData()
       
   def setPinataApiKey(self, api_key):
       self.pinata['api_key'] = api_key
       
   def saveData(self):
       file = open(self.dataFilePath, 'wb')
       data = {'manifest':self.manifest, 'pinata':self.pinata}
       pickle.dump(data, file)
       file.close()

