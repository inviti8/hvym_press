# -*- coding: utf-8 -*-
"""
Created on Wed Mar  1 21:27:28 2023

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

class BeamHandler:
   """
   Class for handling beam
   
   """
   def __init__(self, path, window):
       self.path = path
       self.window = window
       self.loadingWindow = LoadingWindow.LoadingWindow()
       self.beam_path = None
       self.json = os.path.join(self.path, 'download_config.json')
       self.config = DownloadConfigParser.DownloadConfigParser(path, 'beam')
       self.node_folder = None
       self.wallet_folder = None
       self.node_path = None
       self.wallet_path = None
       self.latest_url = None
       self.node = None
       self.node_process = None
       self.node_running = False
       self.node_pool_cmd = None
       self.wallet = None
       self.wallet_process = None
       self.node_process = None
       self.loadingWindow.launchWheel(self.initialize, ())
       
   def initialize(self, *args):
       self.window.disappear()
       self.node_folder = self.config.node_folder
       self.wallet_folder = self.config.wallet_folder
       self.node_path = self.config.node_path
       self.wallet_path = self.config.wallet_path
       self.node_url = self.config.latest_node_url
       self.wallet_url = self.config.latest_wallet_url
       self.node_pool_cmd = self.config.node_pool_cmd
       self.node = self.config.node
       self.wallet = self.config.wallet
           
       if os.path.isfile(self.node) == False:
           folder = os.path.join(self.path, self.config.node_folder)
           dload.save_unzip(self.node_url, folder, True)
               
       if os.path.isfile(self.wallet) == False:
           folder = os.path.join(self.path, self.config.wallet_folder)
           dload.save_unzip(self.wallet_url, folder, True)
               
               
       self.window.reappear()
       
   def start_daemon(self, domain='mainnet', pool=False):
       if self.node_running == True:
           return
       
   def kill_daemon(self):
       if self.node_process == None:
           return
       
       self.node_process.kill()
       self.node_running = False

       
   def open_wallet(self):
       print(self.wallet)
       self.wallet_process = subprocess.Popen('start '+self.wallet, shell=True)