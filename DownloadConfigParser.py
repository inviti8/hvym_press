# -*- coding: utf-8 -*-
"""
Created on Wed Mar  1 21:58:45 2023

@author: pc
"""
import os
import io
import json
from sys import platform

class DownloadConfigParser:
   """
   Class for handling download config parsing
   
   """
   def __init__(self, path, coin):
       self.path = path
       self.json = os.path.join(self.path, 'download_config.json')
       self.coin = coin
       self.config = None
       self.zip_file = None
       self.wallet_zip_file = None
       self.node_zip_file = None
       self.executable_folder = None
       self.wallet_folder = None
       self.node_folder = None
       self.exe_path = None
       self.wallet_path = None
       self.node_path = None
       self.latest_url = None
       self.latest_wallet_url = None
       self.latest_node_url = None
       self.node_pool_cmd = None
       self.node = None
       self.miner = None
       self.wallet = None
       
       with io.open(self.json, mode="r", encoding="utf-8") as f:
           self.config = json.load(f)
           self.zip_file = self.file()
           self.wallet_zip_file = self.file('wallet')
           self.node_zip_file = self.file('node')
           self.executable_folder = self.folder()
           self.wallet_folder = self.folder('wallet')
           self.node_folder = self.folder('node')
           self.exe_path = self.file_path()
           self.wallet_path = self.file_path('wallet')
           self.node_path = self.file_path('node')
           self.latest_url = self.url()
           self.latest_wallet_url = self.url('wallet')
           self.latest_node_url = self.url('node')

           if self.coin == 'dero':
               self.node = os.path.join(self.exe_path, self.config[f'{coin}_executable'][platform]['node'])
               self.miner = os.path.join(self.exe_path, self.config[f'{coin}_executable'][platform]['miner'])
               self.wallet = os.path.join(self.exe_path, self.config[f'{coin}_executable'][platform]['wallet'])
               self.node_pool_cmd = os.path.join(self.node, self.config[f'{coin}_node_pool_cmds'][platform])
           if self.coin == 'beam':
               self.node = os.path.join(self.node_path, self.config[f'{coin}_executable'][platform]['node'])
               self.wallet = os.path.join(self.wallet_path, self.config[f'{coin}_executable'][platform]['wallet'])
               self.node_pool_cmd = os.path.join(self.node, self.config[f'{coin}_node_pool_cmds'][platform])
           
           
   def file(self, app=''):
       
       result = None
       if app != '':
           app = app+'_'
       
       key = f'{self.coin}_{app}zip'

       if key in self.config.keys():
           result = self.config[key][platform]

       return result
   
   def folder(self, app=''):
       result = None
       if self.zip_file != None:
           result = self.zip_file.replace('.tar.gz', '').replace('.zip', '')
       if self.wallet_zip_file != None and app == 'wallet':
           result = self.wallet_zip_file.replace('.tar.gz', '').replace('.zip', '')
       if  self.node_zip_file != None and app == 'node':
           result = self.node_zip_file.replace('.tar.gz', '').replace('.zip', '')

       return result
    
   def file_path(self, app=''):
       result = None
       if self.path != None and self.executable_folder != None and self.zip_file != None:
           result = os.path.join(self.path, self.executable_folder , self.zip_file)
       if self.path != None and self.wallet_folder != None and self.wallet_zip_file != None and app == 'wallet':
           result = os.path.join(self.path, self.wallet_folder, self.wallet_zip_file)
       if self.path != None and self.node_folder != None and self.node_zip_file != None and app == 'node':
           result = os.path.join(self.path, self.node_folder, self.node_zip_file)

       return result
     
   def url(self, app=''):
       result = None
       key = f'{self.coin}_sub_urls'
       sub_url = ''
       url = self.config[f'{self.coin}_latest_url']
       
       if key in self.config.keys():
           sub_url = self.config[key][platform]

       if sub_url != '':
           url = os.path.join(url, sub_url)
       
       if self.zip_file != None:
           result = os.path.join(url, self.zip_file)
       if self.wallet_zip_file != None and app == 'wallet':
            result = os.path.join(url, self.wallet_zip_file)
       if self.node_zip_file != None and app == 'node':
            result = os.path.join(url, self.node_zip_file)

       return result
   
   def wallet_exe(self, app=''):
        result = os.path.join(self.exe_path, self.config[f'{self.coin}_executable'][platform]['wallet'])
        if self.wallet_path != None and app == 'wallet':
            result = os.path.join(self.wallet_path, self.wallet_zip_file)
        if self.node_path != None and app == 'node':
            result = os.path.join(self.node_path, self.node_zip_file)

        return result
   

