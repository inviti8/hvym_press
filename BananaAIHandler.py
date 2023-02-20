# -*- coding: utf-8 -*-
"""
Created on Thu Feb  9 17:48:08 2023

@author: pc
"""
import banana_dev as banana
import PySimpleGUI as sg
import LoadingWindow
import TextUtils
import random
import base64
import json
from youtube_transcript_api import YouTubeTranscriptApi


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
       self.prompts = []
       self.summaryExample = """"[Original]: America has changed dramatically during recent years. Not only has the number of graduates in traditional engineering disciplines such as mechanical, civil, electrical, chemical, and aeronautical engineering declined, but in most of the premier American universities engineering curricula now concentrate on and encourage largely the study of engineering science.  As a result, there are declining offerings in engineering subjects dealing with infrastructure, the environment, and related issues, and greater concentration on high technology subjects, largely supporting increasingly complex scientific developments. While the latter is important, it should not be at the expense of more traditional engineering.
       Rapidly developing economies such as China and India, as well as other industrial countries in Europe and Asia, continue to encourage and advance the teaching of engineering. Both China and India, respectively, graduate six and eight times as many traditional engineers as does the United States. Other industrial countries at minimum maintain their output, while America suffers an increasingly serious decline in the number of engineering graduates and a lack of well-educated engineers. 
       (Source:  Excerpted from Frankel, E.G. (2008, May/June) Change in education: The cost of sacrificing fundamentals. MIT Faculty 
       [Summary]: MIT Professor Emeritus Ernst G. Frankel (2008) has called for a return to a course of study that emphasizes the traditional skills of engineering, noting that the number of American engineering graduates with these skills has fallen sharply when compared to the number coming from other countries. 
       ###
       [Original]: So how do you go about identifying your strengths and weaknesses, and analyzing the opportunities and threats that flow from them? SWOT Analysis is a useful technique that helps you to do this.
       What makes SWOT especially powerful is that, with a little thought, it can help you to uncover opportunities that you would not otherwise have spotted. And by understanding your weaknesses, you can manage and eliminate threats that might otherwise hurt your ability to move forward in your role.
       If you look at yourself using the SWOT framework, you can start to separate yourself from your peers, and further develop the specialized talents and abilities that you need in order to advance your career and to help you achieve your personal goals.
       [Summary]: SWOT Analysis is a technique that helps you identify strengths, weakness, opportunities, and threats. Understanding and managing these factors helps you to develop the abilities you need to achieve your goals and progress in your career.
       ###
       [Original]: A jack-o'-lantern (or jack o'lantern) is a carved lantern, most commonly made from a pumpkin or a root vegetable such as a rutabaga or turnip.[1] Jack-o'-lanterns are associated with the Halloween holiday. Its name comes from the reported phenomenon of strange lights flickering over peat bogs, called will-o'-the-wisps or jack-o'-lanterns. The name is also tied to the Irish legend of Stingy Jack, a drunkard who bargains with Satan and is doomed to roam the Earth with only a hollowed turnip to light his way. 
       Jack-o'-lanterns carved from pumpkins are a yearly Halloween tradition that developed in the United States when Celtic Americans brought their root vegetable carving tradition with them.[2] It is common to see jack-o'-lanterns used as external and internal decorations prior to and on Halloween.
       [Summary]: A jack-o'-lantern is a carved lantern, usually made from a pumpkin or root vegetable like a turnip, associated with Halloween. The tradition originated from Celtic Americans who brought their root vegetable carving tradition to the US. The name comes from strange lights over peat bogs and an Irish legend of Stingy Jack. It is a common decoration for Halloween both inside and outside.
       ####
       [Original]: """
       self.summaryExampleClose = """
       ###
       [Summary]:
       """
    
   def _optimize_chunks(self, chunks):
       idx = 0
       for chunk in chunks:
           if len(chunk.split()) < 250:
               del chunks[idx]
           idx += 1
           
       return chunks
       
   def _add_summary_prompts(self, chunks):
       idx = 1
       length = len(chunks)
       new_chunks = []
       
       for chunk in chunks:
           new_chunk = self.summaryExample + f" {chunk}\n" + self.summaryExampleClose
           new_chunks.append(new_chunk)
           idx += 1
           
       return new_chunks
       
       
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
   
   def launch_gptj(self, prompt, tokens, temp, rep):
        self.seed = None
        self.seeds.clear()
        self.completion = ""
        self.loadingWindow.running = True
        self.loadingWindow.launchWheel(self.gptj_process, prompt, tokens, temp, rep)
        self.loadingWindow.running = False
        
   def gptj_process(self, *args):
       if len(args[0]) > 10:
           self.gptj_complete(args[0], args[1], args[2], args[3])
   
   def gptj_complete(self, prompt, tokens, temp, rep):
       print(self.apiKey)
       print(self.gptjModel)
       
       model_inputs = {
          "max_new_tokens": tokens,
          "temperature": temp,
          "top_probability":1.0,
          "repetition":rep,
          "prompt": prompt
        }
        
       # Run the model
       out = banana.run(self.apiKey, self.gptjModel, model_inputs)
       
       print(out)
        
       #print(out)
       if "output" in out["modelOutputs"][0].keys():
           self.completion += out["modelOutputs"][0]["output"]
       elif "message" in out["modelOutputs"][0].keys():
           self.completion = out["modelOutputs"][0]["message"]
           self.completion = self.completion.replace(prompt, '')
       
       return self.completion
   
   def get_summary(self, text, tokens, temp, rep):
       self.completion = ""
       chunks = TextUtils._chunk_text(text, 1000)
       chunks = self._add_summary_prompts(chunks)
       chunks = self._optimize_chunks(chunks)
       
       prompt = self.summaryExample + f" {text}\n" + self.summaryExampleClose
           
       self.loadingWindow.running = True
       #self.loadingWindow.launchBar(methods, args)
       self.loadingWindow.launchWheel(self.gptj_process, prompt, tokens, temp, rep)
       self.loadingWindow.running = False
       
       for chunk in chunks:
           self.completion = self.completion.replace(chunk, "")
           
       self.completion = self.completion.replace(text, "")
       self.completion = self.completion.replace(self.summaryExample, "")
       self.completion = self.completion.replace(self.summaryExampleClose, "")
       self.completion = self.completion.replace('###', "")
       self.completion = self.completion.replace('[Original]:', "")
       self.completion = self.completion.replace('[Summary]:', "")
       
       print('DONE')
       print(self.completion)
       print('-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-')
       
       return self.completion
           
       
   

