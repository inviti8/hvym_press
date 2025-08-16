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
import urllib.parse

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
       self.mediaDir = '_resources'  # Default fallback
       
   def _deployedURL(self, href):
       """
       Get the deployed IPFS URL for a media file.
       Returns the original href if no deployed URL is found.
       Handles both relative and absolute paths.
       """
       if not self.deployerManifest or 'media_files' not in self.deployerManifest:
           print(f"DEBUG: No manifest or media_files in manifest for {href}")
           return href
       
       # Handle both relative and absolute paths
       filename = os.path.basename(href)
       
       # Decode URL-encoded characters in the filename
       decoded_filename = urllib.parse.unquote(filename)
       
       media_files = self.deployerManifest['media_files']
       
       print(f"DEBUG: Looking for {decoded_filename} (decoded from {filename}) in manifest with {len(media_files)} files")
       print(f"DEBUG: Available files: {list(media_files.keys())}")
       
       # First try exact filename match with decoded name
       if decoded_filename in media_files:
           deployed_url = media_files[decoded_filename]['url']
           print(f"DEBUG: Exact match found for {decoded_filename}: {deployed_url}")
           print(f"Replacing {href} with deployed URL: {deployed_url}")
           return deployed_url
       
       # Try to find by filename regardless of path (case-insensitive)
       for media_filename, media_data in media_files.items():
           if media_filename.lower() == decoded_filename.lower():
               deployed_url = media_data['url']
               print(f"DEBUG: Case-insensitive match found for {decoded_filename}: {deployed_url}")
               print(f"Found media file {decoded_filename} in manifest (case-insensitive match)")
               return deployed_url
       
       # Try to find by filename without extension
       decoded_filename_no_ext = os.path.splitext(decoded_filename)[0]
       for media_filename, media_data in media_files.items():
           media_filename_no_ext = os.path.splitext(media_filename)[0]
           if media_filename_no_ext.lower() == decoded_filename_no_ext.lower():
               deployed_url = media_data['url']
               print(f"DEBUG: Extension-insensitive match found for {decoded_filename}: {deployed_url}")
               print(f"Found media file {decoded_filename} in manifest (extension-insensitive match)")
               return deployed_url
       
       print(f"DEBUG: No deployed URL found for {decoded_filename} (from {href})")
       print(f"DEBUG: Original href: {href}, extracted filename: {filename}, decoded filename: {decoded_filename}")
       print(f"DEBUG: Manifest keys: {list(media_files.keys())}")
       return href
   
   def setMediaDir(self, media_dir):
       """Set the configurable media directory name"""
       self.mediaDir = media_dir
   
   def _handleImgTags(self, html):
        """
        Handle image tags and replace src attributes with deployed URLs.
        Now processes ALL image types, not just .png
        """
        def handleHREF(href):
            result = self._deployedURL(href)
            if result == None:
                result = href
            return result
        
        soup = BeautifulSoup(html, 'html.parser')
        links = soup.findAll('img')
        
        for link in links:
            if 'src' in link.attrs:
                # Process ALL image types, not just .png
                src = link['src']
                if any(ext in src.lower() for ext in ['.png', '.jpg', '.jpeg', '.gif', '.bmp', '.webp']):
                    deployed_src = handleHREF(src)
                    if deployed_src != src:
                        print(f"Replacing image src: {src} -> {deployed_src}")
                        link['src'] = deployed_src
                        link['class'] = 'deployed_img'
                        if link.parent:
                            link.parent['class'] = 'deployed_img_p'
                
        return soup.decode(formatter='html')
        
       
   def _handleMediaTags(self, html):
       """
       Handle media tags (video, audio) and replace href attributes with deployed URLs.
       """
       def handleHREF(href):
           result = self._deployedURL(href)
           if result == None:
               result = href
           return result
               
       soup = BeautifulSoup(html, 'html.parser')
       links = soup.findAll('a')

       for link in links:
           if 'href' in link.attrs:
               href = link['href']
               
               # Handle video files
               if any(ext in href.lower() for ext in ['.mp4', '.avi', '.mov', '.wmv', '.flv', '.webm']):
                   deployed_href = handleHREF(href)
                   if deployed_href != href:
                       print(f"Replacing video href: {href} -> {deployed_href}")
                       new_tag = soup.new_tag('video', controls=None, muted=None, autoplay=None, width="320", height="240", src=deployed_href, type="video/mp4")
                       link.parent['class'] = 'vid_container'
                       link.replaceWith(new_tag)
               
               # Handle audio files
               elif any(ext in href.lower() for ext in ['.mp3', '.wav', '.ogg', '.flac', '.aac']):
                   deployed_href = handleHREF(href)
                   if deployed_href != href:
                       print(f"Replacing audio href: {href} -> {deployed_href}")
                       new_tag = soup.new_tag('audio', controls=None, src=deployed_href, type="audio/mpeg")
                       link.parent['class'] = 'audio_container'
                       link.replaceWith(new_tag)
               
       return soup.decode(formatter='html')
   
   def _shortenMediaLinks(self, html):
       soup = BeautifulSoup(html, 'html.parser')
       imgs = soup.findAll('img')
       links = soup.findAll('a')
        
       for img in imgs:
           if 'src' in img and f'../{self.mediaDir}/' in img['src']:
               img['src'] = img['src'].replace(f'../{self.mediaDir}/', f'./{self.mediaDir}/')  

       for link in links:
           if 'src' in link and ('.mp3' in link['src'] or '.mp4' in link['src']) and f'../{self.mediaDir}/' in link['src']:
               link['src'] = link['src'].replace(f'../{self.mediaDir}/', f'./{self.mediaDir}/')

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
       """
       Generate HTML from markdown file with proper media link replacement.
       
       :param filePath: path to the markdown file
       :type filePath: (str)
       :return: HTML with deployed media links
       :rtype: (str)
       """
       try:
           with open(filePath, 'r', encoding="utf-8") as file:
               md_file = file.read()
           # Fix image paths in markdown BEFORE conversion (for local deployment)
           # Use configurable media directory
           md_file = md_file.replace(f'../{self.mediaDir}/', f'./{self.mediaDir}/')
           
           # Convert markdown to HTML
           html = markdown.markdown(md_file)
           
           # Process media links BEFORE any other HTML manipulation
           html = self._handleImgTags(html)
           html = self._handleMediaTags(html)
           
           return html
           
       except Exception as e:
           print(f"Error generating HTML from {filePath}: {e}")
           return f"<p>Error generating HTML: {e}</p>"
   
   def _renderTemplate(self, template_file, data):
       template = env.get_template(template_file)
       return  template.render(data=data)
   
   def renderPageTemplate(self, template_file, data, page):
        output = self._renderTemplate(template_file, data)
        
        # Debug: Check if the rendered output contains media links
        if f'../{self.mediaDir}/' in output:
            print(f"DEBUG: Rendered template still contains local media links!")
            # Find and show examples
            import re
            media_links = re.findall(f'\\.\\./{re.escape(self.mediaDir)}/[^"\\s]+', output)
            if media_links:
                print(f"DEBUG: Found local media links in template: {media_links[:3]}...")
        else:
            print(f"DEBUG: Rendered template appears to have media links replaced")
        
        # Process with _shortenMediaLinks (expects string)
        output = self._shortenMediaLinks(output)
        
        # Debug: Check after shortening (output is still string)
        if f'../{self.mediaDir}/' in output:
            print(f"DEBUG: After shortening, still contains local media links!")
        else:
            print(f"DEBUG: After shortening, no local media links found")
        
        # Convert to bytes only for file writing
        with open(page, "wb") as f:
            f.write(output.encode())
        
        print(f"DEBUG: Template rendered to: {page}")
        print(f"DEBUG: File size: {len(output)} characters")

   def testMediaReplacement(self, test_html, manifest):
       """
       Test method to verify media link replacement is working correctly.
       
       :param test_html: HTML string to test
       :type test_html: (str)
       :param manifest: Deployment manifest to use
       :type manifest: (dict)
       :return: Processed HTML
       :rtype: (str)
       """
       print("=== TESTING MEDIA REPLACEMENT ===")
       print(f"Input HTML: {test_html}")
       print(f"Manifest: {manifest}")
       
       # Set the manifest
       self.deployerManifest = manifest
       
       # Process the HTML
       result = self._handleImgTags(test_html)
       result = self._handleMediaTags(result)
       
       print(f"Output HTML: {result}")
       print("=== END TEST ===")
       
       return result

