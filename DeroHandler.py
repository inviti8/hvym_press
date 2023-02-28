# -*- coding: utf-8 -*-
"""
Created on Sat Feb 25 17:43:46 2023

@author: pc
"""
import os
import io
import json
import random
import subprocess
from wmi import WMI
from sys import platform
import dload
import LoadingWindow

class DeroHandler:
   """
   Class for handling Dero
   
   """
   def __init__(self, path, window):
       self.path = path
       self.window = window
       self.loadingWindow = LoadingWindow.LoadingWindow()
       self.dero_path = None
       self.json = os.path.join(self.path, 'download_config.json')
       self.config = None
       self.zip_file = None
       self.executable = None
       self.executable_folder = None
       self.executable_path = None
       self.latest_url = None
       self.node = None
       self.node_process = None
       self.node_running = False
       self.node_pool_cmd = None
       self.miner = None
       self.wallet = None
       self.wallet_process = None
       self.loadingWindow.launchWheel(self.initialize, ())
       
       
   def initialize(self, *args):
       self.window.disappear()
       with io.open(self.json, mode="r", encoding="utf-8") as f:
           self.config = json.load(f)
           self.zip_file = self.config['dero_zip'][platform]
           self.executable_folder = self.zip_file.replace('.tar.gz', '').replace('.zip', '')
           self.dero_path = os.path.join(self.path, self.executable_folder)
           self.executable_path = os.path.join(self.dero_path, self.zip_file)
           self.latest_url = os.path.join(self.config['dero_latest_url'], self.zip_file)
           self.node = os.path.join(self.dero_path, self.config['dero_executable'][platform]['node'])
           self.node_pool_cmd = os.path.join(self.node, self.config['dero_node_pool_cmds'][platform])
           self.miner = os.path.join(self.dero_path, self.config['dero_executable'][platform]['miner'])
           self.wallet = os.path.join(self.dero_path, self.config['dero_executable'][platform]['wallet'])
           
           
       if os.path.isfile(self.wallet) == False:
           dload.save_unzip(self.latest_url, self.path, True)
           
       self.window.reappear()
       
   def start_daemon(self, domain='mainnet', pool=False):
       if self.node_running == True:
           return
       
       cmd = self.node
       if pool == True:
           cmd = self.node_pool_cmd
           
       commands = [cmd]
       
       if domain == 'testnet':
            commands = [self.node+' --debug --fastsync']
            
       self.node_process = subprocess.Popen('start '+self.node, shell=True)
       self.node_running = True
       
   def kill_daemon(self):
       if self.node_process == None:
           return
       
       self.node_process.kill()
       self.node_running = False

   
   def get_words(self):
       words_path = os.path.join(self.path, 'words.txt')
       with open(words_path, 'r') as file:
           words = file.read().split()
           words = random.sample(words, 25)
       return words
       
   def open_wallet(self):
       print(self.wallet)
       self.wallet_process = subprocess.Popen('start '+self.wallet, shell=True)
       
   def open_wallet_testnet(self):
       self.wallet_process = subprocess.Popen('start '+self.wallet+' --testnet --debug --rpc-server --rpc-bind=127.0.0.1:10103', shell=True)






       
   def get_device_id(self):
     if platform == "linux" or platform == "linux2":
         my_system = platform.uname().replace(' ', '')
         return '{}-{}'.format(my_system.system, my_system.node)
     elif platform == "darwin":
         my_system = platform.uname().replace(' ', '')
         return '{}-{}'.format(my_system.system, my_system.node)
     elif platform == "win32":
         a = WMI().Win32_ComputerSystemProduct()[0]
         return '{}-{}'.format(a.UUID, a.Name).replace(' ', '')