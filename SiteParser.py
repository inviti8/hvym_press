# -*- coding: utf-8 -*-
"""
Created on Wed Oct 26 18:59:50 2022

@author: pc
"""
import os
from pathlib import Path
from dataclasses import dataclass
from dataclasses_json import dataclass_json
from jinja2 import Environment, FileSystemLoader

SCRIPT_DIR = os.path.abspath( os.path.dirname( __file__ ) )
HOME_PATH = str(Path.home())
file_loader = FileSystemLoader('templates')
env = Environment(loader=file_loader)

@dataclass_json
@dataclass      
class pages:
    '''
    Creates data object to be used in jinja text renderer.
    :param name: String identifier name of element.
    :type name:  (str)
    :param title: Rendered title of element.
    :type title:  (str)
    :param columns: Object for column data.
    :type columns:  (Object)
    :return: (Object) Containing data elements
    :rtype: (Object)
    '''
    name: str
    title: str
    columns: []
    max_height: str
    footer_height: str
    
@dataclass_json
@dataclass      
class cards:
    '''
    Creates data object to be used in jinja text renderer.
    :param name: String identifier name of element.
    :type name:  (str)
    :param title: Rendered title of element.
    :type title:  (str)
    :param html: Rendered title of element.
    :type html:  (str)
    :param columns: Object for column data.
    :type columns:  (Object)
    :return: (Object) Containing data elements
    :rtype: (Object)
    '''
    name: str
    title: str
    html: str
    

class SiteParser:
   'Class for handling site parsing.'
   
   def __init__(self, filePath):
       self.dataFilePath = os.path.join(filePath, 'site.data')
       