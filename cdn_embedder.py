#!/usr/bin/env python3
"""
Fixed CDN Embedder for HVYM Press
This version properly embeds all JavaScript and CSS dependencies without corruption.
"""

import os
import re
import requests
import urllib.parse
from pathlib import Path
import logging
import base64

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class CDNEmbedder:
    def __init__(self, template_path="templates/template_index.txt", output_path="templates/template_index_embedded.txt"):
        self.template_path = template_path
        self.output_path = output_path
        self.downloaded_files = {}
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        })
        
    def download_file(self, url):
        """Download a file and return its content"""
        try:
            logger.info(f"Downloading: {url}")
            response = self.session.get(url, timeout=30)
            response.raise_for_status()
            return response.text
        except Exception as e:
            logger.error(f"Failed to download {url}: {e}")
            return None
    
    def embed_css_files(self, content):
        """Embed CSS files by replacing link tags with style tags"""
        css_pattern = r'<link\s+rel="stylesheet"\s+href="([^"]+)"[^>]*>'
        
        def replace_css(match):
            url = match.group(1)
            if url.startswith('http'):
                css_content = self.download_file(url)
                if css_content:
                    logger.info(f"Embedded CSS: {url}")
                    return f'<style>\n{css_content}\n</style>'
                else:
                    logger.warning(f"Failed to download CSS: {url}")
                    return match.group(0)  # Keep original if download failed
            return match.group(0)  # Keep non-HTTP URLs
        
        return re.sub(css_pattern, replace_css, content)
    
    def embed_js_files(self, content):
        """Embed JavaScript files by replacing script tags with inline script tags"""
        js_pattern = r'<script\s+src="([^"]+)"([^>]*)>'
        
        def replace_js(match):
            url = match.group(1)
            attributes = match.group(2)
            
            if url.startswith('http'):
                js_content = self.download_file(url)
                if js_content:
                    logger.info(f"Embedded JavaScript: {url}")
                    # Clean up the JavaScript content and wrap in CDATA if needed
                    js_content = js_content.strip()
                    if '<!--' in js_content or '-->' in js_content:
                        js_content = f'//<![CDATA[\n{js_content}\n//]]>'
                    return f'<script{attributes}>\n{js_content}\n</script>'
                else:
                    logger.warning(f"Failed to download JavaScript: {url}")
                    return match.group(0)  # Keep original if download failed
            return match.group(0)  # Keep non-HTTP URLs
        
        return re.sub(js_pattern, replace_js, content)
    
    def process_template(self):
        """Process the template and embed all external resources"""
        logger.info(f"Reading template: {self.template_path}")
        
        try:
            with open(self.template_path, 'r', encoding='utf-8') as f:
                content = f.read()
        except Exception as e:
            logger.error(f"Failed to read template: {e}")
            return False
        
        original_size = len(content)
        logger.info(f"Original template size: {original_size:,} bytes")
        
        # Step 1: Embed CSS files
        logger.info("Embedding CSS files...")
        content = self.embed_css_files(content)
        
        # Step 2: Embed JavaScript files
        logger.info("Embedding JavaScript files...")
        content = self.embed_js_files(content)
        
        # Step 3: Write the embedded template
        logger.info(f"Writing embedded template: {self.output_path}")
        try:
            with open(self.output_path, 'w', encoding='utf-8') as f:
                f.write(content)
        except Exception as e:
            logger.error(f"Failed to write output: {e}")
            return False
        
        final_size = len(content)
        logger.info(f"Final template size: {final_size:,} bytes")
        logger.info(f"Size increase: {final_size - original_size:,} bytes")
        
        return True
    
    def verify_embedding(self):
        """Verify that all external resources were embedded"""
        logger.info("Verifying embedding...")
        
        try:
            with open(self.output_path, 'r', encoding='utf-8') as f:
                content = f.read()
        except Exception as e:
            logger.error(f"Failed to read output for verification: {e}")
            return False
        
        # Check for remaining external CSS links
        css_links = re.findall(r'<link\s+rel="stylesheet"\s+href="([^"]+)"', content)
        external_css = [url for url in css_links if url.startswith('http')]
        
        # Check for remaining external script tags
        script_srcs = re.findall(r'<script\s+src="([^"]+)"', content)
        external_scripts = [url for url in script_srcs if url.startswith('http')]
        
        logger.info(f"Remaining external CSS: {len(external_css)}")
        logger.info(f"Remaining external scripts: {len(external_scripts)}")
        
        if external_css:
            logger.warning("External CSS still present:")
            for url in external_css:
                logger.warning(f"  - {url}")
        
        if external_scripts:
            logger.warning("External scripts still present:")
            for url in external_scripts:
                logger.warning(f"  - {url}")
        
        if not external_css and not external_scripts:
            logger.info("✅ All external resources successfully embedded!")
            return True
        else:
            logger.warning("⚠️ Some external resources remain")
            return False

def main():
    """Main function to run the fixed CDN embedder"""
    embedder = FixedCDNEmbedder()
    
    print("🔧 Fixed CDN Embedder for HVYM Press")
    print("=" * 50)
    
    # Process the template
    if embedder.process_template():
        print("✅ Template processing completed successfully!")
        
        # Verify the embedding
        if embedder.verify_embedding():
            print("🎉 All external resources successfully embedded!")
            print(f"📁 Output file: {embedder.output_path}")
        else:
            print("⚠️ Some external resources may not have been embedded")
    else:
        print("❌ Template processing failed!")
        return 1
    
    return 0

if __name__ == "__main__":
    exit(main())
