# -*- coding: utf-8 -*-
"""
Created on Thu Feb  9 17:48:08 2023

@author: pc
"""
import os
from pathlib import Path
import banana_dev as banana
import base64
from io import BytesIO
from PIL import Image


SCRIPT_DIR = os.path.abspath( os.path.dirname( __file__ ) )



class BananaAIHandler:
   """
   Class for handling Banana AI calls
   
   """
   def __init__(self, apiKey, diffusionModel, gptjModel, resourcePath):
       self.apiKey = apiKey
       self.diffusionModel = diffusionModel
       self.gptjModel = gptjModel
       
       def get_img(self, prompt, width, height, seed):
            model_inputs = {
            	"prompt": prompt,
            	"num_inference_steps":50,
            	"guidance_scale":9,
            	"height":height,
            	"width":width,
            	"seed":seed
            }
            
            api_key = self.apiKey
            model_key = self.diffusionModel
            
            # Run the model
            out = banana.run(api_key, model_key, model_inputs)
            
            # Extract the image and save to output.jpg
            image_byte_string = out["modelOutputs"][0]["image_base64"]
            image_encoded = image_byte_string.encode('utf-8')
            image_bytes = BytesIO(base64.b64decode(image_encoded))
            image = Image.open(image_bytes)
            image.save("output.jpg")
