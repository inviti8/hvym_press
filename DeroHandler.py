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
       self.fast_sync = ' --fastsync --add-exclusive-node=minernode1.dero.live:11011'
       self.loadingWindow.launchWheel(self.initialize, ())
       
       
   def initialize(self, *args):
       self.window.disappear()
       self.latest_url = self.config.latest_url
       self.node_pool_cmd = self.config.node_pool_cmd
       self.node = self.config.node
       self.miner = self.config.miner
       self.wallet = self.config.wallet
           
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
           
       commands = [cmd]
       
       if domain == 'testnet':
            cmd = 'start '+self.node+' --debug --testnet --fastsync'
            
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

