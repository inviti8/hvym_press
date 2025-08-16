# -*- coding: utf-8 -*-
""" """
import os, shutil
import subprocess
import concurrent.futures
from subprocess import run, Popen, PIPE
from pathlib import Path
import ast
import platform


class HVYM_Handler:
    """
    Class for handling hvym calls
    """

    def __init__(self):
        self.HOME = os.path.expanduser("~")
        self.bin = os.path.join(self.HOME, ".local", "share", "heavymeta-cli", "hvym")

    def _get_command_array(self, command):
        """Convert shell command to platform-specific command array"""
        if platform.system() == "Windows":
            return ["cmd", "/c", command]
        else:
            return ["bash", "-c", command]

    def _run_futures_cmds(self, cmds):
        result = None
        with concurrent.futures.ThreadPoolExecutor() as executor:
            # Use platform-specific command arrays instead of shell=True
            futures = {
                executor.submit(run, self._get_command_array(cmd)): cmd for cmd in cmds
            }

            for future in concurrent.futures.as_completed(futures):
                cmd = futures[future]

                try:
                    result = future.result()  # Get the result from Future object

                except (
                    Exception
                ) as e:  # Checking for any exception raised by the command
                    print("Command failed with error:", str(e))

            return result

    def _run_command(self, cmd):
        # Use platform-specific command array instead of shell=True
        process = Popen(self._get_command_array(cmd), stdout=PIPE, stderr=PIPE)
        output, error = process.communicate()

        if process.returncode != 0:  # Checking the return code
            print("Command failed with error:", error.decode("utf-8"))
        else:
            print(output.decode("utf-8"))
            return output.decode("utf-8")

    def _subprocess(self, command):
        try:
            # Use platform-specific command array instead of shell=True
            output = subprocess.check_output(
                self._get_command_array(command), stderr=subprocess.STDOUT
            )
            return output.decode("utf-8")
        except Exception as e:
            print(f"An error occured: {e}")
            return None

    def choice_popup(self, msg):
        return self._run_command(f'{self.bin} custom-choice-prompt "{msg}"').rstrip()

    def loading_msg(self, msg):
        self._run_command(f'{self.bin} custom-loading-msg "{msg}"')

    def prompt(self, msg):
        self._run_command(f'{self.bin} custom-prompt "{msg}"')
