# -*- coding: utf-8 -*-
"""
Created on Thu Nov 10 09:29:06 2022

@author: pc
"""
import os
import markdown
from PIL import Image
from bs4 import BeautifulSoup
from jinja2 import Environment, FileSystemLoader

SCRIPT_DIR = os.path.abspath( os.path.dirname( __file__ ) )
templates = os.path.join(SCRIPT_DIR , 'templates')
file_loader = FileSystemLoader(templates)
env = Environment(loader=file_loader)


class MarkdownHandler:
   """
   Class for handling conversion
   of .md to html
   
   """
   def __init__(self, filePath, deployerManifest=None):
       self.filePath = filePath
       self.deployerManifest = deployerManifest
       
   def _deployedURL(self, href):
       result = None
       f_name = os.path.basename(href)

       if self.deployerManifest != None and f_name in self.deployerManifest.keys():
           if self.deployerManifest[f_name]['url'] != None:
               result = self.deployerManifest[f_name]['url']
               
       return result
   
   def _handleImgTags(self, html):
        def handleHREF(href):
            result = self._deployedURL(href)
               
            if result == None:
                result = href
                
            return result
        
        soup = BeautifulSoup(html, 'html.parser')
        links = soup.findAll('img')
        
        for link in links:
            if '.png' in link['src']:
                src = handleHREF(link['src'])
                f_name = os.path.basename(src)
                st = "width:100%;"
                   
                new_tag = soup.new_tag('img', alt=f_name, src=src, style=st)
                link['class'] = 'deployed_img'
                link.parent['class'] = 'deployed_img_p'
                link.replaceWith(new_tag)
                
        return soup.decode(formatter='html')
        
       
   def _handleMediaTags(self, html):
       
       def handleHREF(href):
           result = self._deployedURL(href)
              
           if result == None:
               result = href
               
           return result
               
       soup = BeautifulSoup(html, 'html.parser')
       links = soup.findAll('a')

       for link in links:
           
           if '.mp4' in link['href']:
               href = handleHREF(link['href'])
                  
               new_tag = soup.new_tag('video', controls=None, muted=None, autoplay=None, width="320", height="240", src=href, type="video/mp4")
               new_tag['src'] = href
               link.parent['class'] = 'vid_container'
               link.replaceWith(new_tag)
               
           if '.mp3' in link['href']:
               href = handleHREF(link['href'])
               
               new_tag = soup.new_tag('audio', controls=None, src=href, type="audio/mpeg")
               link.parent['class'] = 'audio_container'
               link.replaceWith(new_tag)
               
       return soup.decode(formatter='html')
   
   def _shortenMediaLinks(self, html):
       soup = BeautifulSoup(html, 'html.parser')
       imgs = soup.findAll('img')
       links = soup.findAll('a')
        
       for img in imgs:
           if 'src' in img and '../' in img['src']:
               img['src'] = img['src'].replace('../', './')  

       for link in links:
           if ('src' in link and ('.mp3' in link['src'] or '.mp4' in link['src'])) and ('src' in img and '../' in img['src']):
               link['src'] = link['src'].replace('../', './')

       return soup.decode(formatter='html')
   
   def _flattenMediaLinks(self, html, resource_dir):
       soup = BeautifulSoup(html, 'html.parser')
       imgs = soup.findAll('img')
       links = soup.findAll('a')
        
       for img in imgs:
           if 'src' in img and f'../{resource_dir}/' in img['src']:
               img['src'] = img['src'].replace(f'../{resource_dir}/', '')  

       for link in links:
           if ('src' in link and ('.mp3' in link['src'] or '.mp4' in link['src'])) and ('src' in img and f'../{resource_dir}/' in img['src']):
               link['src'] = link['src'].replace(f'../{resource_dir}/', '')

       return soup.decode(formatter='html')
   
   def updateDeployerManifest(self, manifest):
       self.deployerManifest = manifest
   
   def generateHTML(self, filePath):
       file = open(filePath, 'r', encoding="utf-8")
       md_file = file.read()
       md = markdown.Markdown()
       md.convert(md_file)
       html = markdown.markdown(md_file)
       html = self._handleMediaTags(html)
       html = self._handleImgTags(html)
       file.close()
       
       return md.convert(html)
   
   def _renderTemplate(self, template_file, data):
       template = env.get_template(template_file)
       return  template.render(data=data)
   
   def renderPageTemplate(self, template_file, data, page):
        output = self._renderTemplate(template_file, data)
        output = self._shortenMediaLinks(output.encode())
        
        with open(page, "wb") as f:
            f.write(output.encode())

   def renderICPPageTemplate(self, template_file, data, page, resource_dir):
        output = self._renderTemplate(template_file, data)
        output = self._flattenMediaLinks(output.encode(), resource_dir)
        
        with open(page, "wb") as f:
            f.write(output.encode())