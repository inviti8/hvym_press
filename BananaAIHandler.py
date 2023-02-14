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
   def __init__(self, apiKey, diffusionModel, autoDiffusionModel, gptjModel, resourcePath):
       self.apiKey = apiKey
       self.diffusionModel = diffusionModel
       self.autoDiffusionModel = autoDiffusionModel
       self.diffusion_inputs = {}
       self.gptjModel = gptjModel
       
   def txt2img(self, prompt, width, height, seed, inference, sampling, guidance):
       print(self.apiKey)
       print(self.autoDiffusionModel)
       
       self.diffusion_inputs = {
           "endpoint": "txt2img",
           "params": {
               "prompt": prompt,
               "steps":inference,
               "sampler_name": sampling,
               "cfg_scale":guidance,
               "height":height,
               "width":width,
               "seed":seed
               }
        }

         
       # Run the model
       out = banana.run(self.apiKey, self.autoDiffusionModel, self.diffusion_inputs)
       
       print(out)
        

       return out["modelOutputs"][0]["images"][0]
   
   def img2img(self, img, prompt, width, height, seed, inference, sampling, guidance):
       print(self.apiKey)
       print(self.autoDiffusionModel)
       print('------------------------------------------------------')
       print(img)
       print('------------------------------------------------------')
       
       self.diffusion_inputs = {
           "endpoint": "img2img",
           "params": {
               "prompt": prompt,
               "steps":inference,
               "sampler_name": sampling,
               "cfg_scale":guidance,
               "height":height,
               "width":width,
               "seed":seed,
               "init_images": [
                    img
                ]
               }
        }

         
       # Run the model
       out = banana.run(self.apiKey, self.autoDiffusionModel, self.diffusion_inputs)
       
       print(out)
        

       return out["modelOutputs"][0]["images"][0]
       
       
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
   

