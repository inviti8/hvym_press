# -*- coding: utf-8 -*-
"""
Created on Wed Feb  8 21:32:36 2023

@author: pc
"""
import os
import sys
import json
import requests
import hashlib
import cryptography
from cryptography.fernet import Fernet
import LoadingWindow

SCRIPT_DIR = os.path.abspath( os.path.dirname( __file__ ) )



class KeyHandler:
   """
   Class for handling Banana AI
   
   """
   def __init__(self, appID, key, deviceID):
       self.appID = appID
       self.key = key
       self.deviceID = deviceID
       self.bananaAPI = None
       self.diffusionModel = None
       self.autoDiffusionModel = None
       self.gptjModel = None
       self.api_url = 'https://notable-excellent-skill.anvil.app/'
       sha = hashlib.sha1(self.deviceID.encode(encoding = 'UTF-8'))
       device_hex = sha.hexdigest()
       sha = hashlib.sha1(self.key.encode(encoding = 'UTF-8'))
       key_hex = sha.hexdigest()
       self.url = self.api_url+'_/api/authenticate/'+device_hex+'&'+key_hex+'&'+appID
       self.getKeys()
       # self.loadingWindow = LoadingWindow.LoadingWindow()
       # self.loadingWindow.launchMethod(self.getKeys, ())
       
   def getKeys(self, *args):
       headers = {
           }
               
       response = requests.request("POST", self.url, headers=headers)
       data = response.json()
       f = Fernet(self.key)
       self.bananaAPI = f.decrypt(data['banana'].encode(encoding = 'UTF-8'))
       self.diffusionModel = f.decrypt(data['diffusion'].encode(encoding = 'UTF-8'))
       self.autoDiffusionModel = f.decrypt(data['auto-diffusion'].encode(encoding = 'UTF-8'))
       self.gptjModel = f.decrypt(data['gptj'].encode(encoding = 'UTF-8'))
       self.bananaAPI = self.bananaAPI.decode(encoding = 'UTF-8')
       self.diffusionModel = self.diffusionModel.decode(encoding = 'UTF-8')
       self.autoDiffusionModel = self.autoDiffusionModel.decode(encoding = 'UTF-8')
       self.gptjModel = self.gptjModel.decode(encoding = 'UTF-8')

       
