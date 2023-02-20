# -*- coding: utf-8 -*-
"""
Created on Sun Feb 19 18:08:31 2023

@author: pc
"""

import os
import openai
import re
import LoadingWindow

class OpenAIHandler:
   """
   Class for handling Open AI calls
   
   """
   def __init__(self, apiKey, resourcePath):
       self.apiKey = apiKey
       self.model = 'text-davinci-003'
       self.loadingWindow = LoadingWindow.LoadingWindow()
       self.completion = ""
       
       openai.organization = "org-kMSNeN3xvkEtj73QeFtVfekp"
       openai.api_key = self.apiKey
       openai.Model.retrieve(self.model)
       
   def _optimize_prompt(self, prompt):
       # Remove unnecessary words
       prompt = re.sub(r'\b(the|a|an|is|are|do|does|did|will|would|should)\b', '', prompt)
      
       # Remove unnecessary punctuation
       prompt = re.sub(r'[^\w\s]', '', prompt)
        
       return prompt
   
    
   def launch_get_summary(self, prompt, tokens, temp):
        self.completion = ""
        self.loadingWindow.running = True
        self.loadingWindow.launchWheel(self.get_text_summary, prompt, tokens, temp)
        self.loadingWindow.running = False
    
   def get_text_summary(self, text, tokens=128, temp=0.7, num_sentences='2 or 3', tone='fun', agreement='agrees'):
      prompt = f"Summarize the following text in {num_sentences} sentences. Please write in a {tone} tone that {agreement} with the speaker:\n"
      summary = ""
      full_prompt = prompt+text
      
      completion = openai.Completion.create(
        model=self.model,
        prompt=full_prompt,
        max_tokens=tokens,
        temperature=temp
      )
    
      cost = completion['usage']['total_tokens']
    
      summary = summary + completion['choices'][0]['text']
      
      self.completion += summary
    
      #transaction = app_tables.transactions.get(id=id)
      #transaction['cost'] += cost
      
      return summary