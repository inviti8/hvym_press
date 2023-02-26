# -*- coding: utf-8 -*-
"""
Created on Sat Feb 25 17:43:46 2023

@author: pc
"""
import os
import io
import json
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
       self.miner = None
       self.wallet = None
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
           self.miner = os.path.join(self.dero_path, self.config['dero_executable'][platform]['miner'])
           self.wallet = os.path.join(self.dero_path, self.config['dero_executable'][platform]['wallet'])
           
       if os.path.isfile(self.wallet) == False:
           dload.save_unzip(self.latest_url, self.path, True)
           
       self.window.reappear()
       
   def create_new_wallet(self):
       print(self.wallet)
       # Launch the CLI program as a subprocess
       # process = subprocess.Popen([self.wallet], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True)
        
       # # Send input to the subprocess to select option 2
       # process.stdin.write("2\n")
       # process.stdin.flush()
        
       # # Read the output from the subprocess
       # output, errors = process.communicate()
        
       # # Print the output and errors (if any)
       # print("Output: ", output)
       # print("Errors: ", errors)






       
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