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
       self.completion = ""
       
   def _add_summary_prompts(self, chunks):
       idx = 1
       length = len(chunks)
       new_chunks = []
       
       for chunk in chunks:
           new_chunk = f"For the following Text, Return a summary point {idx} of {length} for an article outline. Text:{chunk}."
           new_chunks.append(new_chunk)
           idx += 1
           
       return new_chunks
       
   def _chunk_text(self, text, size):
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
       
   def launch_txt2img(self, values):
       self.seed = None
       self.seeds.clear()
       self.png_b64.clear()
       self.loadingWindow.running = True
       self.loadingWindow.launchWheel(self.txt2img_process, values)
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
       
       info = json.loads(out["modelOutputs"][0]["info"])
       self.seed = info["seed"]
       self.seeds = info["all_seeds"]
        

       return out["modelOutputs"][0]["images"]
   
   def launch_img2img(self, values):
        self.seed = None
        self.seeds.clear()
        self.png_b64.clear()
        self.loadingWindow.running = True
        self.loadingWindow.launchWheel(self.img2img_process, values)
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
   
   def launch_gptj(self, prompt, tokens):
        self.seed = None
        self.seeds.clear()
        self.completion = None
        self.loadingWindow.running = True
        print(prompt)
        self.loadingWindow.launchWheel(self.gptj_process, prompt, tokens)
        self.loadingWindow.running = False
        
   def gptj_process(self, *args):
       print(args)
       print('[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[')
       if len(args[0]) > 10:
           self.gptj_complete(args[0], args[1])
   
   def gptj_complete(self, prompt, tokens):
       print(self.apiKey)
       print(self.gptjModel)
       
       model_inputs = {
          "max_new_tokens": tokens,
          "prompt": prompt
        }
        
       # Run the model
       out = banana.run(self.apiKey, self.gptjModel, model_inputs)
        
       print(out)
       if "output" in out["modelOutputs"][0].keys():
           self.completion += out["modelOutputs"][0]["output"]
       elif "message" in out["modelOutputs"][0].keys():
           self.completion = out["modelOutputs"][0]["message"]
       
       return self.completion
   
   def get_summary(self, text):
       chunks = self._chunk_text(text, 500)
       chunks = self._add_summary_prompts(chunks)
       methods = []
       args = []
       
       for i in range(len(chunks)):
           methods.append(self.gptj_process)
           args.append((chunks[i], 128))
           
       self.loadingWindow.running = True
       self.loadingWindow.launchBar(methods, args)
       self.loadingWindow.running = False
       
       print('DONE')
       print(self.completion)
       print('-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-')
       
       return self.completion
           
       
   

