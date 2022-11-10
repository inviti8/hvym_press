# -*- coding: utf-8 -*-
"""
Created on Thu Nov 10 09:29:06 2022

@author: pc
"""
import os
import markdown
from pathlib import Path
from PIL import Image
from bs4 import BeautifulSoup
from jinja2 import Environment, FileSystemLoader

SCRIPT_DIR = os.path.abspath( os.path.dirname( __file__ ) )
HOME_PATH = str(Path.home())
file_loader = FileSystemLoader('templates')
env = Environment(loader=file_loader)


class MarkdownHandler:
   """
   Class for handling conversion
   of .md to html
   
   """
   def __init__(self, filePath):
       self.filePath = filePath
       
   def _handleMediaTags(self, html):
       soup = BeautifulSoup(html, 'html.parser')
       links = soup.findAll('a')

       for link in links:
           if '.mp4' in link['href']:
               new_tag = soup.new_tag('video', controls=None, muted=None, autoplay=None, width="320", height="240", src=link['href'], type="video/mp4")
               link.parent['class'] = 'vid_container'
               link.replaceWith(new_tag)
               
           if '.mp3' in link['href']:
               new_tag = soup.new_tag('audio', controls=None, src=link['href'], type="audio/mpeg")
               link.parent['class'] = 'audio_container'
               link.replaceWith(new_tag)
               
       return soup.decode(formatter='html')
   
   def generateHTML(self, filePath):
       file = open(filePath, 'r', encoding="utf-8")
       md_file = file.read()
       md = markdown.Markdown()
       md.convert(md_file)
       html = markdown.markdown(md_file)
       html = self._handleMediaTags(html)
       file.close()
       
       return md.convert(html)
   
   def renderPageTemplate(self, template_file, data, page):

        template = env.get_template(template_file)
        output = template.render(data=data)
        
        with open(page, "wb") as f:
            f.write(output.encode())