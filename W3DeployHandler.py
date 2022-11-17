# -*- coding: utf-8 -*-
"""
Created on Tue Nov  8 13:27:01 2022

@author: meta-cronos

A class for handling web content deployment.
"""

import os
import pickle
import requests
import markdown
from PIL import Image
from json import dumps
from pathlib import Path
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
    fileType: str
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
   
   def __init__(self, filePath, dirName, settings):
       self.resourcePath = os.path.join(filePath, dirName)
       self.files = os.listdir(self.resourcePath)
       self.dataFilePath = os.path.join(filePath, 'deploy.data')
       self.manifest = {}
       self.pinata = {'api_url':"https://managed.mypinata.cloud/api/v1/content", 'jwt':settings['pinata_jwt'], 'api_key':settings['pinata_key'], 'gateway':settings['pinata_gateway']}
       self.deployFolder = []
       
       if os.path.isfile(self.dataFilePath):
           dataFile = open(self.dataFilePath, 'rb')
           data = pickle.load(dataFile)
           self.manifest = data['manifest']
           self.pinata = data['pinata']

       self.updateManifestData(filePath)
       
       # print(self.files)
       print(self.manifest)
       print(self.pinata)
       
   def _folderArray(self, parentPath, filePath, basePath):
       paths = os.listdir(filePath)
       
       for f in paths:
           full_path = os.path.join(filePath, f).replace('\\', '/')
           f_name = full_path.replace(basePath, '').replace('\\', '/')
           
           if os.path.isdir(full_path):
               self._folderArray(full_path, full_path, basePath)
           else:
               self.deployFolder.append(('file',(f_name,open(full_path,'rb'),'application/octet-stream')))
               
   def pinFiles(self, files, payload):
       url = "https://api.pinata.cloud/pinning/pinFileToIPFS"
       
       headers = {
         'Authorization': "Bearer "+self.pinata['jwt']
       }
       
       response = requests.request("POST", url, headers=headers, data=payload, files=files)
       
       return response.text
       
       
   def pinFile(self, fileName, filePath, fileType, payload):
       url = "https://api.pinata.cloud/pinning/pinFileToIPFS"

       files=[
         ('file',(fileName,open(filePath,'rb'),fileType))
       ]
       headers = {
         'Authorization': "Bearer "+self.pinata['jwt']
       }
       
       response = requests.request("POST", url, headers=headers, data=payload, files=files)
       
       return response.text
       
   def newFileData(self, filePath):
       f_type = None
       return {'time_stamp':'', 'type':f_type, 'path':filePath, 'url':None}
   
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

