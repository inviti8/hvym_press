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
import threading
import cryptography
from pathlib import Path
from jinja2 import Environment, FileSystemLoader
import PySimpleGUI as sg
import LoadingWindow

SCRIPT_DIR = os.path.abspath( os.path.dirname( __file__ ) )
file_loader = FileSystemLoader('templates')
env = Environment(loader=file_loader)


class KeyHandler:
   """
   Class for handling Banana AI
   
   """
   def __init__(self, appID, key, deviceID):
       self.appID = appID
       self.key = key
       self.deviceID = deviceID
       self.api_url = 'https://notable-excellent-skill.anvil.app/'
       sha = hashlib.sha1(self.deviceID.encode(encoding = 'UTF-8'))
       device_hex = sha.hexdigest()
       sha = hashlib.sha1(self.key.encode(encoding = 'UTF-8'))
       key_hex = sha.hexdigest()
       self.url = self.api_url+'_/api/authenticate/'+device_hex+'&'+key_hex+'&'+appID
       self.loadingWindow = LoadingWindow.LoadingWindow()
       self.loadingWindow.launchMethod(self.getKeys, ())
       
   def getKeys(self, *args):
       print('GetKeys')
       headers = {
           }
               
       response = requests.request("POST", self.url, headers=headers)
       print(response.text)
