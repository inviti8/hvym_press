# -*- coding: utf-8 -*-
"""
"""
import os, shutil
import subprocess
import concurrent.futures
from subprocess import run, Popen, PIPE
from pathlib import Path
import ast


class HVYM_Handler:
   """
   Class for handling hvym calls
   """
   def __init__(self):
       self.HOME = os.path.expanduser('~')
       self.icp_daemon_running = False
       self.bin = os.path.join(self.HOME, '.local', 'share', 'heavymeta-cli', 'hvym')
       self.icp_path = os.path.join(self.HOME, '.local', 'share', 'heavymeta-cli', 'icp')
       self.icp_template = self.icp_site_template()
       self.icp_session = self.current_icp_session()
       self.icp_project_path = None
       self.icp_assets_path = None
       self.icp_index_path = None

   def _run_futures_cmds(self, cmds):
    result = None
    with concurrent.futures.ThreadPoolExecutor() as executor:
        futures = {executor.submit(run, cmd, shell=True): cmd for cmd in cmds}
        
        for future in concurrent.futures.as_completed(futures):
            cmd = futures[future]
            
            try:
                result = future.result()  # Get the result from Future object
                
            except Exception as e:   # Checking for any exception raised by the command
                print("Command failed with error:", str(e))

        return result
    
   def _run_command(self, cmd):
    process = Popen(cmd, stdout=PIPE, stderr=PIPE, shell=True)
    output, error = process.communicate()

    if process.returncode != 0:   # Checking the return code
        print("Command failed with error:", error.decode('utf-8'))
    else:
        print(output.decode('utf-8'))
        return output.decode('utf-8')

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
       self.icp_assets_path = os.path.join(self.icp_project_path, 'assets', 'assets').rstrip()
       self.icp_index_path = os.path.join(self.icp_project_path, 'assets', 'src', 'index.html').rstrip()
       return self.icp_project_path
   
   def install_icp_site_template(self):
       self._subprocess(f'{self.bin} icp-init assets -f')

   def start_icp_daemon(self):
       output = self._run_futures_cmds([f'{self.bin} icp-start-assets assets'])
       self.icp_daemon_running = True
       print(output)

   def stop_icp_daemon(self):
       output = self._run_futures_cmds([f'{self.bin} icp-stop-assets assets'])
       self.icp_daemon_running = False
       print(output)

   def _icp_deploy(self, debug=True):
       cmd = f'{self.bin} icp-deploy-assets assets'
       urls = ast.literal_eval(self._run_command(cmd))
    
       return urls[1].rstrip()

   def debug_icp_deploy(self):
       return self._icp_deploy()

   def icp_deploy(self):
       return self._icp_deploy(False)

   def clean_icp_assets(self):
       if os.path.isdir(self.icp_assets_path):
        for filename in os.listdir(self.icp_assets_path):
            file_path = os.path.join(self.icp_assets_path, filename)
            try:
                if os.path.isfile(file_path) or os.path.islink(file_path):
                    os.unlink(file_path)
                elif os.path.isdir(file_path):
                    shutil.rmtree(file_path)
            except Exception as e:
                print('Failed to delete %s. Reason: %s' % (file_path, e))

   def choice_popup(self, msg):
       return self._run_command(f'{self.bin} custom-choice-prompt "{msg}"').rstrip()
   
   def loading_msg(self, msg):
       self._run_command(f'{self.bin} custom-loading-msg "{msg}"')

   def prompt(self, msg):
       self._run_command(f'{self.bin} custom-prompt "{msg}"')
       