# -*- coding: utf-8 -*-
"""
"""
import os
import subprocess


SCRIPT_DIR = os.path.abspath( os.path.dirname( __file__ ) )

class HVYM_Handler:
   """
   Class for handling hvym calls
   """
   def __init__(self):
       self.HOME = HOME = os.path.expanduser('~')
       self.bin = os.path.join(self.HOME, '.local', 'share', 'heavymeta-cli', 'hvym')
       self.icp_path = os.path.join(self.HOME, '.local', 'share', 'heavymeta-cli', 'icp')
       self.icp_template = self.icp_site_template()
       self.icp_session = self.current_icp_session()
       self.icp_project_path = None

   def _subprocess(self, command):
        try:
            output = subprocess.check_output(command, shell=True, stderr=subprocess.STDOUT)
            return output.decode('utf-8')
        except Exception as e:
            print(f'An error occured: {e}')
            return None
        
   def icp_site_template(self):
       return self._subprocess(f'{self.bin} icp-template assets').rstrip()
        
   def current_icp_session(self):
       return self._subprocess(f'{self.bin} icp-project-path')
   
   def set_icp_session(self, name):
       self.icp_session = self._subprocess(f'{self.bin} icp-project {name}').rstrip()
       return self.icp_session
   
   def set_icp_project_path(self):
       self.icp_project_path = os.path.join(self.icp_session, self.icp_template).rstrip()
       return self.icp_project_path
   
   def install_icp_site_template(self):
       self._subprocess(f'{self.bin} icp-init assets -f')

   def start_icp_daemon(self):
       self._subprocess(f'{self.bin} icp-start-assets assets')

   def stop_icp_daemon(self):
       self._subprocess(f'{self.bin} icp-stop-assets assets')