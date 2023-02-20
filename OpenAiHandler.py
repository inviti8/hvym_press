# -*- coding: utf-8 -*-
"""
Created on Sun Feb 19 18:08:31 2023

@author: pc
"""

import os
import openai
import re
import LoadingWindow
import TextUtils
from youtube_transcript_api import YouTubeTranscriptApi

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
       
   
   def _get_youtube_transcript(self, url):
       vid_id = url.replace('https://www.youtube.com/watch?v=', '')
       ts = YouTubeTranscriptApi.get_transcript(vid_id)
       text = ""
            
       for ob in ts:
          if '[Music]' not in ob['text'] and '[Applause]' not in ob['text']:
             text=text+' '+ob['text']+'. '
             
       chunks = TextUtils._chunk_text(text, 500)
       
       return chunks
   
   def launch_completion(self, prompt, tokens, temp):
        self.completion = ""
        self.loadingWindow.running = True
        self.loadingWindow.launchWheel(self.get_completion, prompt, tokens, temp)
        self.loadingWindow.running = False
   
   def get_completion(self, prompt, tokens=128, temp=0.7, num_sentences='2 or 3', tone='fun', agreement='agrees'):
      summary = ""
      
      completion = openai.Completion.create(
        model=self.model,
        prompt=prompt,
        max_tokens=tokens,
        temperature=temp
      )
    
      cost = completion['usage']['total_tokens']
    
      summary = completion['choices'][0]['text']
      
      self.completion += summary
      
      return summary
   
    
   def launch_get_summary(self, prompt, tokens, temp):
        self.completion = ""
        self.loadingWindow.running = True
        self.loadingWindow.launchWheel(self.get_text_summary, prompt, tokens, temp)
        self.loadingWindow.running = False
        
    
   def launch_get_large_summary(self, text, tokens, temp, num_sentences, tone, agreement):
        self.completion = ""
        paragraphs = TextUtils._separate_paragraphs(text)
        methods = []
        args = []
        
        for i in range(len(paragraphs)):
            methods.append(self.get_text_summary)
            args.append((paragraphs[i], tokens, temp, num_sentences, tone, agreement))

        
        self.loadingWindow.running = True
        self.loadingWindow.launchBar(methods, args)
        #self.loadingWindow.launchWheel(self.get_text_summary, prompt, tokens, temp)
        self.loadingWindow.running = False
        
        return self.completion
    
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