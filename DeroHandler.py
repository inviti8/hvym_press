# -*- coding: utf-8 -*-
"""
Created on Sat Feb 25 17:43:46 2023

@author: pc
"""
import os
import io
import json
import random
import requests
import subprocess
from wmi import WMI
from sys import platform
import dload
import LoadingWindow
import DownloadConfigParser
from json import dumps
from dataclasses import dataclass
from dataclasses_json import dataclass_json
from dataclasses import dataclass, asdict, field

@dataclass_json
@dataclass
class DeroAsset:
   """
   Class for a dero asset
   :param startSupply: Starting supply of collection.'
   :type startSupply:  (Uint64)
   :param decimals: ?'
   :type decimals:  (Uint64)
   :param collection: Linked collection id.'
   :type collection:  (String)
   :param metadataFormat: Format of the metadat, example: json'
   :type metadataFormat:  (String)
   :param metadata: metadata for the asset.'
   :type metadata:  (String)
   :param freezeCollection: Variable to freeze the collection.'
   :type freezeCollection:  (Uint64)
   :param freezeMetadata: Variable to freeze the metadata.'
   :type freezeMetadata:  (Uint64)
   """
   startSupply: int
   decimals: int
   collection: str
   metadataFormat: str
   metadata: str
   freezeCollection:int
   freezeMetadata:int
   
   @property
   def dictionary(self):
       return asdict(self)

   @property
   def json(self):
       return dumps(self.dictionary)
   

@dataclass_json
@dataclass
class DeroAssetCollection:
   """
   Class for a dero collection
   :param metadataFormat: Format of the metadat, example: json'
   :type metadataFormat:  (String)
   :param metadata: metadata for the asset.'
   :type metadata:  (String)
   :param freezeMetadata: Variable to freeze the metadata.'
   :type freezeMetadata:  (Uint64)
   """
   metadataFormat: str
   metadata: str
   freezeMetadata:int
   
   @property
   def dictionary(self):
       return asdict(self)

   @property
   def json(self):
       return dumps(self.dictionary)

class DeroHandler:
   """
   Class for handling Dero
   
   """
   def __init__(self, path, window):
       self.path = path
       self.cmd_json = os.path.join(self.path, 'command_config.json')
       self.cmd_config = None
       self.window = window
       self.loadingWindow = LoadingWindow.LoadingWindow()
       self.config = DownloadConfigParser.DownloadConfigParser(path, 'dero')
       self.node = None
       self.node_process = None
       self.node_running = False
       self.node_pool_cmd = None
       self.miner = None
       self.wallet = None
       self.wallet_process = None
       self.simulator = None
       self.fast_sync = ' --fastsync --add-exclusive-node=minernode1.dero.live:11011'
       self.loadingWindow.launchWheel(self.initialize, ())
       self.nft_collection_template = os.path.join(path, 'dero-contracts', 'g45-c.bas')
       self.nft_asset_template = os.path.join(path, 'dero-contracts', 'g45-at.bas')
       self.nft_collection = None
       self.nft_asset = None
       self.cmd_sync_time = None
       self.cmd_restart_time = None
       
       with io.open(self.cmd_json, mode="r", encoding="utf-8") as f:
           self.cmd_config = json.load(f)
           self.cmd_sync_time = self.cmd_config['time_sync_cmds'][platform]['sync_time']
           self.cmd_restart_time = self.cmd_config['time_sync_cmds'][platform]['restart_time']
       
   def initialize(self, *args):
       self.window.disappear()
       self.latest_url = self.config.latest_url
       self.node_pool_cmd = self.config.node_pool_cmd
       self.node = self.config.node
       self.miner = self.config.miner
       self.wallet = self.config.wallet
       self.simulator = self.config.simulator
       self.nft_collection = os.path.join(self.config.exe_path, 'g45-c.bas')
       self.nft_asset = os.path.join(self.config.exe_path, 'g45-at.bas')
           
       if os.path.isfile(self.wallet) == False:
           dload.save_unzip(self.latest_url, self.path, True)
           
       self.window.reappear()
       
   def sync_time(self):   
       self.node_process = subprocess.Popen(self.cmd_sync_time, shell=True)
       
   def restart_time(self):   
       self.node_process = subprocess.Popen(self.cmd_restart_time, shell=True)
       
   def fastsync_daemon(self):
       if self.node_running == True:
           return
       self.node_process = subprocess.Popen('start '+self.node+self.fast_sync, shell=True)
       self.node_running = True
       
   def start_daemon(self, domain='mainnet', pool=False):
       if self.node_running == True:
           return
       
       cmd = 'start '+self.node
       if pool == True:
           cmd = self.node_pool_cmd
       
       if domain == 'testnet':
            cmd = 'start '+self.simulator
            
       self.node_process = subprocess.Popen(cmd, shell=True)
       self.node_running = True
       
   def kill_daemon(self):
       if self.node_process == None:
           return
       
       self.node_process.kill()
       self.node_running = False
       
   def open_wallet(self):
       self.wallet_process = subprocess.Popen('start '+self.wallet, shell=True)
       
   def open_wallet_testnet(self):
       self.wallet_process = subprocess.Popen('start '+self.wallet+' --testnet --debug --rpc-server --rpc-bind=127.0.0.1:10103', shell=True)
   
   def deploy_nft_asset(self):
       self.deploy_nft(self, self.nft_asset, '10103')
       
   def deploy_nft_collection(self):
       self.deploy_nft(self, self.nft_collection, '10103')
       
   def deploy_test_nft_asset(self):
       self.deploy_nft(self, self.nft_asset, '30000')
       
   def deploy_test_nft_collection(self):
       self.deploy_nft(self, self.nft_collection, '30000')
   
   def deploy_nft(self, nft_template, port):
       result = False
       url = f'http://127.0.0.1:{port}/install_sc'
       headers = {'Content-Type': 'application/octet-stream'}
       with open(nft_template, 'rb') as f:
           data = f.read()
        
       try:
           response = requests.post(url, headers=headers, data=data)
           print(response.text)
           if response.status_code == 200:
               result = True
       except:
            print('Not Connected')
            
       return result
        
       
   def ping(self, port):
       result = False
       url = f'http://127.0.0.1:{port}/json_rpc'
       headers = {"Content-Type": "application/json"}
       payload = {
            "jsonrpc": "2.0",
            "id": "1",
            "method": "DERO.Ping"
       }
       
       try:
           response = requests.post(url, headers=headers, json=payload)
           if response.status_code == 200:
               result = True
           print(response.status_code)
       except:
           print('Not connected')
           
       return result
           

