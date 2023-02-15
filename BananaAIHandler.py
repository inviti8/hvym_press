# -*- coding: utf-8 -*-
"""
Created on Thu Feb  9 17:48:08 2023

@author: pc
"""
import banana_dev as banana
import PySimpleGUI as sg
import LoadingWindow
import random
import base64
import json



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
       self.seed = None
       self.seeds = []
       self.png_b64 = []
       self.loadingWindow = LoadingWindow.LoadingWindow()
       
   def launch_txt2img(self, values):
       self.seed = None
       self.seeds.clear()
       self.png_b64.clear()
       self.loadingWindow.launchMethod(self.txt2img_process, values)
       self.loadingWindow.running = False
       
   def txt2img_process(self, values):
       img_seed = int(values['seed'])
       
       if len(values['prompt']) > 10:
           if values['randomize-vars'] == True:
               img_seed = int(random.randint(0, 2**32 - 1))
               
           prompt = values['prompt'] + values['modifier-text'] + values['tag-text'] + values['artist-text']
           self.png_b64 = self.txt2img(prompt, values['img-width'], values['img-height'], img_seed, values['img-variations'], values['inference-steps'], values['mod-sampling'], values['guidance-scale'])
           
               
       
   def txt2img(self, prompt, width, height, seed, batch_size, inference, sampling, guidance):
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
               "seed":seed,
               "batch_size":batch_size
               }
        }

         
       # Run the model
       out = banana.run(self.apiKey, self.autoDiffusionModel, self.diffusion_inputs)
       
       print(out)
       
       info = json.loads(out["modelOutputs"][0]["info"])
       self.seed = info["seed"]
       self.seeds = info["all_seeds"]
        

       return out["modelOutputs"][0]["images"]
   
   def launch_img2img(self, values):
        self.seed = None
        self.seeds.clear()
        self.png_b64.clear()
        self.loadingWindow.launchMethod(self.img2img_process, values)
        self.loadingWindow.running = False
   
    
   def img2img_process(self, values):
       image_file = open(values['ai-img-in'], "rb")
       bs64_str = base64.b64encode(image_file.read())
       bs64_str = str(bs64_str.decode(encoding = 'UTF-8'))
       img_seed = int(values['seed'])
       
       if len(values['prompt']) > 10:
           if values['randomize-vars'] == True:
               img_seed = int(random.randint(0, 2**32 - 1))
               
           prompt = values['prompt'] + values['modifier-text'] + values['tag-text'] + values['artist-text']
           self.png_b64 = self.img2img(bs64_str, prompt, values['img-width'], values['img-height'], img_seed, values['img-variations'], values['inference-steps'], values['mod-sampling'], values['guidance-scale'])
   
   def img2img(self, img, prompt, width, height, seed, batch_size, inference, sampling, guidance):
       print(self.apiKey)
       print(self.autoDiffusionModel)
       
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
               "batch_size":batch_size,
               "init_images": [
                    img
                ]
               }
        }

         
       # Run the model
       out = banana.run(self.apiKey, self.autoDiffusionModel, self.diffusion_inputs)
       
       print(out)
       
       info = json.loads(out["modelOutputs"][0]["info"])
       self.seed = info["seed"]
       self.seeds = info["all_seeds"]
        

       return out["modelOutputs"][0]["images"]
       
       
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
   

