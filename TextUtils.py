# -*- coding: utf-8 -*-
"""
Created on Sun Feb 19 22:49:09 2023

@author: pc
"""
import re

def _separate_paragraphs(text_block):
     # Split the text_block into individual paragraphs
     paragraphs = text_block.split("\n\n")
 
     # Remove any leading or trailing whitespace from each paragraph
     paragraphs = [p.strip() for p in paragraphs]
 
     # Remove any empty paragraphs
     paragraphs = [p for p in paragraphs if p]
 
     # Return the list of paragraphs
     return paragraphs
 
def _optimize_prompt(prompt):
    # Remove unnecessary words
    prompt = re.sub(r'\b(the|a|an|is|are|do|does|did|will|would|should)\b', '', prompt)
   
    # Remove unnecessary punctuation
    prompt = re.sub(r'[^\w\s]', '', prompt)
     
    return prompt

def _chunk_text(text, size):
    words = text.split()
    chunks = []
    current_chunk = ""

    for word in words:
        if len(current_chunk) + len(word) > size:
            chunks.append(current_chunk)
            current_chunk = ""
  
        current_chunk += word + " "
          
    current_chunk = current_chunk
    chunks.append(current_chunk)
  
    return chunks