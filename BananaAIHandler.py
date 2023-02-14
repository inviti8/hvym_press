# -*- coding: utf-8 -*-
"""
Created on Thu Feb  9 17:48:08 2023

@author: pc
"""
import banana_dev as banana
import PySimpleGUI as sg
import LoadingWindow
import random



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
       self.seeds = []
       self.png_b64 = []
       self.loadingWindow = LoadingWindow.LoadingWindow()
       
   def launch_txt2img(self, values):
       self.seeds.clear()
       self.png_b64.clear()
       self.loadingWindow.launchMethod(self.txt2img_process, values)
       self.loadingWindow.running = False
       
   def txt2img_process(self, values):
       img_seed = int(values['seed'])
       
       if len(values['prompt']) > 10:
           for i in range(values['img-variations']):
               if values['randomize-vars'] == True:
                   img_seed = int(random.randint(0, 2**32 - 1))
                   
               prompt = values['prompt'] + values['modifier-text'] + values['tag-text'] + values['artist-text']
               img_str = self.txt2img(prompt, values['img-width'], values['img-height'], img_seed, values['inference-steps'], values['mod-sampling'], values['guidance-scale'])
               self.seeds.append(img_seed)
               self.png_b64.append(img_str)
       
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
   

