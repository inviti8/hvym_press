# -*- coding: utf-8 -*-
"""
Created on Sat Feb 25 17:43:46 2023

@author: pc
"""
import os
import io
import random
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
       
       
   def initialize(self, *args):
       self.window.disappear()
       self.latest_url = self.config.latest_url
       self.node_pool_cmd = self.config.node_pool_cmd
       self.node = self.config.node
       self.miner = self.config.miner
       self.wallet = self.config.wallet
       self.simulator = self.config.simulator
           
       if os.path.isfile(self.wallet) == False:
           dload.save_unzip(self.latest_url, self.path, True)
           
       self.window.reappear()
       
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
       print(self.wallet)
       self.wallet_process = subprocess.Popen('start '+self.wallet, shell=True)
       
   def open_wallet_testnet(self):
       self.wallet_process = subprocess.Popen('start '+self.wallet+' --testnet --debug --rpc-server --rpc-bind=127.0.0.1:10103', shell=True)

