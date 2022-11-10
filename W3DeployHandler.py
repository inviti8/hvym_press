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
from pathlib import Path
from PIL import Image
from jinja2 import Environment, FileSystemLoader

SCRIPT_DIR = os.path.abspath( os.path.dirname( __file__ ) )
HOME_PATH = str(Path.home())
file_loader = FileSystemLoader('templates')
env = Environment(loader=file_loader)


class W3DeployHandler:
   """
   Class for handling deploy data,
   and deployment of files.
   
   """
   
   def __init__(self, filePath, settings):
       self.files = os.listdir(filePath)
       self.dataFilePath = os.path.join(filePath, 'deploy.data')
       self.manifest = {}
       self.pinata = {'api_url':"https://managed.mypinata.cloud/api/v1/content", 'api_key':settings['pinata_key'], 'gateway':['pinata_gateway']}
       
       if os.path.isfile(self.dataFilePath):
           dataFile = open(self.dataFilePath, 'rb')
           data = pickle.load(dataFile)
           self.manifest = data['manifest']
           self.pinata = data['pinata']

       self.updateManifestData(filePath)
       
       # print(self.files)
       # print(self.manifest)
       
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
       self.pinata = {'api_url':"https://managed.mypinata.cloud/api/v1/content", 'api_key':settings['pinata_key'], 'gateway':['pinata_gateway']}
       self.saveData()
       
   def setPinataApiKey(self, api_key):
       self.pinata['api_key'] = api_key
       
   def saveData(self):
       file = open(self.dataFilePath, 'wb')
       data = {'manifest':self.manifest, 'pinata':self.pinata}
       pickle.dump(data, file)
       file.close()

