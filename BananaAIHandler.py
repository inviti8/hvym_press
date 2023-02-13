# -*- coding: utf-8 -*-
"""
Created on Thu Feb  9 17:48:08 2023

@author: pc
"""
import banana_dev as banana
import PySimpleGUI as sg



class BananaAIHandler:
   """
   Class for handling Banana AI calls
   
   """
   def __init__(self, apiKey, diffusionModel, gptjModel, resourcePath):
       self.apiKey = apiKey
       self.diffusionModel = diffusionModel
       self.diffusion_inputs = {}
       self.gptjModel = gptjModel
       
       
   def get_img(self, prompt, width, height, seed, inference, guidance):
       print(self.apiKey)
       print(self.diffusionModel)
       
       self.diffusion_inputs = {
         "prompt": prompt,
         "num_inference_steps":inference,
         "guidance_scale":guidance,
         "height":height,
         "width":width,
         "seed":seed
        }

         
       # Run the model
       out = banana.run(self.apiKey, self.diffusionModel, self.diffusion_inputs)
        

       return out["modelOutputs"][0]["image_base64"]

